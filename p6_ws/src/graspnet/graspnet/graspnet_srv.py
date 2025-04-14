import os
import sys
import PIL.Image
import numpy as np
import open3d as o3d
import argparse
import scipy.io as scio
import PIL

import torch
from graspnetAPI import GraspGroup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(ROOT_DIR, '..'))

sys.path.append(os.path.join(PARENT_DIR, 'models'))
sys.path.append(os.path.join(PARENT_DIR, 'dataset'))
sys.path.append(os.path.join(PARENT_DIR, 'utils'))

from graspnet import GraspNet, pred_decode
from graspnet_dataset import GraspNetDataset
from collision_detector import ModelFreeCollisionDetector
from data_utils import CameraInfo, create_point_cloud_from_depth_image

# OpenCV
import cv2
from cv_bridge import CvBridge

# ROS Stuff
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from project_interfaces.srv import GetGrasp

#Image Segmenetation
from ultralytics import YOLOWorld
from ultralytics import SAM


parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint_path', help='Model checkpoint path')
parser.add_argument('--num_point', type=int, default=20000, help='Point Number [default: 20000]')
parser.add_argument('--num_view', type=int, default=300, help='View Number [default: 300]')
parser.add_argument('--collision_thresh', type=float, default=0.01, help='Collision Threshold in collision detection [default: 0.01]')
parser.add_argument('--voxel_size', type=float, default=0.01, help='Voxel Size to process point clouds before collision detection [default: 0.01]')
cfgs = parser.parse_args()

class RealSenseCamera(Node):
    def __init__(self):
        super().__init__('realsense_subscriber_node')
        self.color_img = None
        self.depth_img = None

        # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/aligned_depth_to_color/image_raw',  # Topic name
            self.convert_to_depth_img,  # Callback function
            10  # Queue size
        )
        
         # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/color/image_raw',  # Topic name
            self.convert_to_color_img,  # Callback function
            10  # Queue size
        )

        self.bridge = CvBridge()

    def convert_to_depth_img(self, msg):
        # Convert the ROS Image message to OpenCV image (16-bit single-channel)
        self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

    def convert_to_color_img(self, msg):
        # Convert the ROS Image message to an OpenCV image
        self.color_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
        #self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR) 


class AnyGraspPipeline(Node):
    def __init__(self):
        super().__init__('anygrasp_node')
        self.realsense_camera = RealSenseCamera()

        self.grasp_srv = self.create_service(GetGrasp, 'get_grasp_anygrasp', self.get_grasps)

        #Frames for depth and color
        self.depth_frame = None   
        self.color_frame = None
        self.retrieve_aligned_frames()


    def retrieve_aligned_frames(self):      
        # Retrieve aligned frames from the RealSense camera by spinning the node untill new frames are available
        while self.realsense_camera.depth_img is None or self.realsense_camera.color_img is None:
                rclpy.spin_once(self.realsense_camera)

        while np.array_equal(self.realsense_camera.depth_img, self.depth_frame) or np.array_equal(self.realsense_camera.color_img, self.color_frame):
                rclpy.spin_once(self.realsense_camera)
        
        self.depth_frame = self.realsense_camera.depth_img
        self.color_frame = self.realsense_camera.color_img

    def get_grasps(self, request, response):
        self.retrieve_aligned_frames()

        gripper = request.gripper
        if (gripper == "right" or gripper == "Right"):
             width = 0.155
        elif (gripper == "left" or gripper == "Left"):
             width = 0.085
        else:
             response.log = "Invalid gripper choice, pick either 'right' or 'left'."
             return response

        net = get_net()
        end_points, cloud = get_and_process_data(self.color_frame, self.depth_frame)
        gg = get_grasps(net, end_points, width)
        if cfgs.collision_thresh > 0:
            gg = collision_detection(gg, np.array(cloud.points))
        vis_grasps(gg, cloud)
        
        # Pick only the highest rated grasp
        gg.nms()
        gg.sort_by_score()
        gg = gg[:1]
        
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


def get_net():
    # Init the model
    net = GraspNet(input_feature_dim=0, num_view=cfgs.num_view, num_angle=12, num_depth=4,
            cylinder_radius=0.05, hmin=-0.02, hmax_list=[0.01,0.02,0.03,0.04], is_training=False)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)
    # Load checkpoint
    install_path = get_package_share_directory('graspnet')
    src_path = install_path.replace('install', 'src').split('share')[0]
    checkpoint_path = os.path.join(src_path, 'logs', 'log_kn', 'checkpoint-rs.tar')
    
    checkpoint = torch.load(checkpoint_path)
    net.load_state_dict(checkpoint['model_state_dict'])
    start_epoch = checkpoint['epoch']
    print("-> loaded checkpoint %s (epoch: %d)"%(checkpoint_path, start_epoch))
    # set model to eval mode
    net.eval()
    return net

def get_and_process_data(img, depth_img):
    # load data
    color = img / 255.0
    depth = depth_img

    object_name = 'book'

    # Compute workspace_mask using YOLO & SAM
    model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes
    model.set_classes([object_name])  # Set the class list to only include the specified object
        
    # Execute inference with the YOLOv8l-world model on the specified image
    yolo_results = model.predict(img, verbose=False) #, conf = 0.3

    mask_binary = None
    if len(yolo_results[0].boxes.data) > 0:  # Check if there are any detected objects
        for i in range(len(yolo_results[0].boxes.data)): # for each detected object it finds grasp poses
                x_min, y_min, x_max, y_max, _ , _ = yolo_results[0].boxes.data[i]  #_, _ = confidence and class

                sam = SAM("sam_b.pt")
                results = sam.predict(img, stream=False, bboxes=[x_min, y_min, x_max, y_max], points=None, labels=None)
                sam_masks = (results[0].masks.data.cpu().numpy()*255).astype(np.uint8)
                
                #convert the mask to binary
                mask_binary = (sam_masks > 0).astype(np.uint8)
                mask_binary = np.squeeze(mask_binary)  # From shape (1, H, W) → (H, W)
    else:
         print("YoloWorld failed to detect object.")

    mask_binary = mask_binary.astype(np.bool_)

    # Intrinsic camera parameters
    intrinsic = np.array([
        [909.85,   0.0, 645.60],
        [  0.0, 909.57, 386.57],
        [  0.0,   0.0,   1.0]
    ])

    # mm to meters
    factor_depth = np.array([1000.0])

    # generate cloud
    camera = CameraInfo(1280.0, 720.0, intrinsic[0][0], intrinsic[1][1], intrinsic[0][2], intrinsic[1][2], factor_depth)
    cloud = create_point_cloud_from_depth_image(depth, camera, organized=True)

    # get valid points
    mask = (mask_binary & (depth > 0))
    cloud_masked = cloud[mask]
    color_masked = color[mask]

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

def get_grasps(net, end_points, width):
    # Forward pass
    with torch.no_grad():
        end_points = net(end_points)
        grasp_preds = pred_decode(end_points, gripper_max_width=width)
    gg_array = grasp_preds[0].detach().cpu().numpy()
    gg = GraspGroup(gg_array)
    return gg

def collision_detection(gg, cloud):
    mfcdetector = ModelFreeCollisionDetector(cloud, voxel_size=cfgs.voxel_size)
    collision_mask = mfcdetector.detect(gg, approach_dist=0.05, collision_thresh=cfgs.collision_thresh)
    gg = gg[~collision_mask]
    return gg

def vis_grasps(gg, cloud):
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
    