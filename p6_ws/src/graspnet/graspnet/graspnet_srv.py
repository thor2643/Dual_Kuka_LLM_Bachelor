# Imports
import os
import sys
import numpy as np
import open3d as o3d
import argparse
import logging
logging.getLogger().setLevel(logging.ERROR) # Supress warnings

# GraspNet / AnyGrasp
import torch
from graspnetAPI import GraspGroup
from graspnet import GraspNet, pred_decode
from graspnet_dataset import GraspNetDataset
from collision_detector import ModelFreeCollisionDetector
from data_utils import CameraInfo, create_point_cloud_from_depth_image

# ROS Stuff
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from project_interfaces.srv import GetGrasp
from cv_bridge import CvBridge

# Image Segmenetation
from ultralytics import YOLOWorld
from ultralytics import SAM


# Arguments parsed to AnyGrasp.
parser = argparse.ArgumentParser()
parser.add_argument('--num_point', type=int, default=20000, help='Point Number [default: 20000]')
parser.add_argument('--num_view', type=int, default=300, help='View Number [default: 300]')
parser.add_argument('--collision_thresh', type=float, default=0.01, help='Collision Threshold in collision detection [default: 0.01]')
parser.add_argument('--voxel_size', type=float, default=0.01, help='Voxel Size to process point clouds before collision detection [default: 0.01]')
cfgs = parser.parse_args()

# Determine the location of "graspnet" folder using ROS2 inferstructure
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..'))

sys.path.append(os.path.join(PARENT_DIR, 'models'))
sys.path.append(os.path.join(PARENT_DIR, 'dataset'))
sys.path.append(os.path.join(PARENT_DIR, 'utils'))

class RealSenseCamera(Node):
    def __init__(self):
        super().__init__('realsense_subscriber_node')
        self.color_img = None
        self.depth_img = None
        self.bridge = CvBridge()

        # Create subsriber nodes to camera
        self.create_subscription(
            Image, '/camera/camera/aligned_depth_to_color/image_raw', self.convert_to_depth_img, 10
        )
        self.create_subscription(
            Image, '/camera/camera/color/image_raw', self.convert_to_color_img, 10
        )

        # Removed subscriber to CameraInfo, as K matrix is constant.

    # Create callback functions
    def convert_to_depth_img(self, msg):
        # Convert the ROS Image message to OpenCV image (16-bit single-channel)
        self.get_logger().info("Received depth image")
        self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

    def convert_to_color_img(self, msg):
        # Convert the ROS Image message to an OpenCV image, NOTE: AnyGrasp uses RGB
        self.get_logger().info("Received color image")
        self.color_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")


class AnyGraspPipeline(Node):
    def __init__(self):
        super().__init__('anygrasp_node')

        # Insatantiate the RealSense Camera.
        self.realsense_camera = RealSenseCamera()

        # Frames for depth and color
        self.depth_frame = None   
        self.color_frame = None
        self.color = None
        self.mask_binary = None
        self.width = None

        # Intrinsic camera parameters & mm -> m factor
        self.intrinsic = np.array([
            [909.85,   0.0, 645.60],
            [  0.0, 909.57, 386.57],
            [  0.0,   0.0,   1.0]
        ])
        self.factor_depth = np.array([1000.0])

        self.grasp_srv = self.create_service(GetGrasp, 'get_grasp_anygrasp', self.get_grasps)


    # Callback for image capture
    def retrieve_aligned_frames(self):  
        self.realsense_camera.depth_img = None
        self.realsense_camera.color_img = None

        # Retrieve aligned frames from the RealSense camera by spinning the node untill new frames are available
        while self.realsense_camera.depth_img is None or self.realsense_camera.color_img is None:
                rclpy.spin_once(self.realsense_camera)

        while np.array_equal(self.realsense_camera.depth_img, self.depth_frame) or np.array_equal(self.realsense_camera.color_img, self.color_frame):
                rclpy.spin_once(self.realsense_camera)
        
        self.depth_frame = self.realsense_camera.depth_img
        self.color_frame = self.realsense_camera.color_img
        self.color = self.color_frame / 255.0


    def get_grasps(self, request, response):
        # Get image
        self.retrieve_aligned_frames()

        # Check what gripper will be used for grasping
        gripper = request.gripper
        if (gripper == "right" or gripper == "Right"):
             self.width = 0.155
        elif (gripper == "left" or gripper == "Left"):
             self.width = 0.085
        else:
             response.log = "Invalid gripper choice, pick either 'right' or 'left'"
             return response
        

        # Use YOLOWorld and SAM for segmenetation
        flag = self.get_object_information(request)
        self.get_logger().info(f'Flag is {flag}')
        if flag == False:
            response.log = f"YOLOWorld failed to detect any {request.object_name}. However, {self.objects_found} was found!"
            return response

        # Run the neural network AnyGrasp
        net = self.get_net()
        end_points, cloud = self.get_and_process_data()
        gg = self.infer_grasps(net, end_points)
        if cfgs.collision_thresh > 0:
            gg = self.collision_detection(gg, np.array(cloud.points))
        
        # -- Debug feature
        #self.vis_grasps(gg, cloud)
        
        # Determine the best grasp candidate.
        gg.nms()
        gg.sort_by_score()
        gg = gg[:1]
        
        # Fill ROS message with grasp information and return.
        if len(gg) > 0:
            top_grasp = gg[0]

            response.grasp_candidates = [
            float(top_grasp.score),
            float(top_grasp.width),
            float(top_grasp.height),
            float(top_grasp.depth),
            *[float(v) for v in top_grasp.translation],
            *[float(v) for v in np.array(top_grasp.rotation_matrix).flatten()]
        ]
            response.log = "Grasp extracted successfully."
        else:
            response.log = "No valid grasp found."
        return response


    def get_object_information(self, request):
        det_object = request.object_name
        mask_binary = None
        
        #Compute workspace_mask using YOLO & SAM
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes
        sam = SAM("sam_b.pt")

        model.set_classes([det_object])  # Set the class list to only include the specified object
            
        # Execute inference with the YOLOv8l-world model on the specified image
        yolo_results = model.predict(self.color_frame, verbose=False) #, conf = 0.3

        # Sanity check - Was object detected?
        if len(yolo_results[0].boxes.data) > 0:
            for i in range(len(yolo_results[0].boxes.data)): # for each detected object it finds grasp poses
                x_min, y_min, x_max, y_max, _ , _ = yolo_results[0].boxes.data[i]  #_, _ = confidence and class

                sam_results = sam.predict(self.color_frame, stream=False, bboxes=[x_min, y_min, x_max, y_max], points=None, labels=None)
                sam_masks = (sam_results[0].masks.data.cpu().numpy()*255).astype(np.uint8)
                
                #convert the mask to binary
                mask_binary = (sam_masks > 0).astype(np.uint8)
                mask_binary = np.squeeze(mask_binary)  # From shape (1, H, W) → (H, W)
            self.mask_binary = mask_binary.astype(np.bool_)
            return True
        else:
            self.objects_found = []
            for i in range(len(yolo_results[0].boxes.data)):
                self.objects_found.append(model.names[int(yolo_results[0].boxes.data[i][5])])
            
            self.get_logger().info(f'YOLOWorld failed to detect {det_object}, but found {self.objects_found}')
            return False


    def get_net(self):
        # Init the model
        net = GraspNet(input_feature_dim=0, num_view=cfgs.num_view, num_angle=12, num_depth=4,
                cylinder_radius=0.05, hmin=-0.02, hmax_list=[0.01,0.02,0.03,0.04], is_training=False)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        net.to(device)

        # Load checkpoint using ROS structure
        install_path = get_package_share_directory('graspnet')
        src_path = install_path.replace('install', 'src').split('share')[0]
        checkpoint_path = os.path.join(src_path, 'logs', 'log_kn', 'checkpoint-rs.tar')
        # Using pre-configured RealSense checkpoint

        checkpoint = torch.load(checkpoint_path)
        net.load_state_dict(checkpoint['model_state_dict'])
        start_epoch = checkpoint['epoch']
        print("-> loaded checkpoint %s (epoch: %d)"%(checkpoint_path, start_epoch))
        
        # Set model to eval mode
        net.eval()
        return net

    def get_and_process_data(self):
        # generate cloud
        camera = CameraInfo(1280.0, 720.0, self.intrinsic[0][0], self.intrinsic[1][1], self.intrinsic[0][2], self.intrinsic[1][2], self.factor_depth)
        cloud = create_point_cloud_from_depth_image(self.depth_frame, camera, organized=True)

        # get valid points
        mask = (self.mask_binary & (self.depth_frame > 0))
        cloud_masked = cloud[mask]
        color_masked = self.color[mask]

        # sample points
        if len(cloud_masked) >= cfgs.num_point:
            idxs = np.random.choice(len(cloud_masked), cfgs.num_point, replace=False)
        else:
            idxs1 = np.arange(len(cloud_masked))
            idxs2 = np.random.choice(len(cloud_masked), cfgs.num_point-len(cloud_masked), replace=True)
            idxs = np.concatenate([idxs1, idxs2], axis=0)
        cloud_sampled = cloud_masked[idxs]
        color_sampled = color_masked[idxs]

        # convert data
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(cloud_masked.astype(np.float32))
        cloud.colors = o3d.utility.Vector3dVector(color_masked.astype(np.float32))
        end_points = dict()
        cloud_sampled = torch.from_numpy(cloud_sampled[np.newaxis].astype(np.float32))
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        cloud_sampled = cloud_sampled.to(device)
        end_points['point_clouds'] = cloud_sampled
        end_points['cloud_colors'] = color_sampled

        return end_points, cloud

    def infer_grasps(self, net, end_points):
        # Forward pass
        with torch.no_grad():
            end_points = net(end_points)
            grasp_preds = pred_decode(end_points, gripper_max_width=self.width)
        gg_array = grasp_preds[0].detach().cpu().numpy()
        gg = GraspGroup(gg_array)
        return gg

    def collision_detection(self, gg, cloud):
        mfcdetector = ModelFreeCollisionDetector(cloud, voxel_size=cfgs.voxel_size)
        collision_mask = mfcdetector.detect(gg, approach_dist=0.05, collision_thresh=cfgs.collision_thresh)
        gg = gg[~collision_mask]
        return gg

    # No longer used, but debug feature for visualising grasp!
    def vis_grasps(self, gg, cloud):
        gg.nms()
        gg.sort_by_score()
        gg = gg[:1]
        grippers = gg.to_open3d_geometry_list()
        o3d.visualization.draw_geometries([cloud, *grippers])


def main(args=None):
    rclpy.init(args=args)
    graspnetinstance = AnyGraspPipeline()
    rclpy.spin(graspnetinstance) 
    rclpy.shutdown()

if __name__=='__main__':
    main()
    