# Imports
import os
import sys
import numpy as np
import open3d as o3d
import argparse
from scipy.spatial.transform import Rotation as R
import cv2

# GraspNet / AnyGrasp
import torch
from graspnetAPI import GraspGroup, RectGraspGroup
from graspnet import GraspNet, pred_decode
from graspnet_dataset import GraspNetDataset
from collision_detector import ModelFreeCollisionDetector
from data_utils import CameraInfo, create_point_cloud_from_depth_image

# ROS Stuff
from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from project_interfaces.srv import GetObjectInfo
from project_interfaces.msg import Grasp6D, DetectedObject, TransformMatrix
from cv_bridge import CvBridge
from geometry_msgs.msg import Point, Vector3

# Image Segmenetation
from ultralytics import YOLOWorld
from ultralytics import SAM


# Arguments parsed to AnyGrasp.
parser = argparse.ArgumentParser()
parser.add_argument('--num_point', type=int, default=40000, help='Point Number [default: 20000]')
parser.add_argument('--num_view', type=int, default=300, help='View Number [default: 300]')
parser.add_argument('--collision_thresh', type=float, default=0.01, help='Collision Threshold in collision detection [default: 0.01]')
parser.add_argument('--voxel_size', type=float, default=0.01, help='Voxel Size to process point clouds before collision detection [default: 0.01]')
cfgs, _ = parser.parse_known_args()

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
        self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

    def convert_to_color_img(self, msg):
        # Convert the ROS Image message to an OpenCV image, NOTE: AnyGrasp uses RGB
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
        self.cv2img = None
        self.mask_binary = None
        self.width = None
        self.transformation_matrix = None

        # Intrinsic camera parameters & mm -> m factor
        self.intrinsic = np.array([
            [909.85,   0.0, 645.60],
            [  0.0, 909.57, 386.57],
            [  0.0,   0.0,   1.0]
        ])
        self.factor_depth = np.array([1000.0])

        self.grasp_srv = self.create_service(GetObjectInfo, 'get_any_object_info', self.get_grasps)

        self.image_publisher = self.create_publisher(Image, 'video_frames', 10)


    def get_grasps(self, request, response):
        print("GraspNet-Baseline Service Called")
        self.transformation_matrix = np.array(request.transform.matrix).reshape((4, 4))  
        # Get image
        self.retrieve_aligned_frames()

        # Check what gripper will be used for grasping
        gripper = request.gripper
        if (gripper == "right" or gripper == "Right"):
             self.width = 0.155
        elif (gripper == "left" or gripper == "Left"):
             self.width = 0.085
        else:
             print("Error occoured during choice of gripper")
             return response
        

        # Use YOLOWorld and SAM for segmenetation
        flag = self.get_object_information(request, response)
        if flag == False:
            return response

        # Run the neural network AnyGrasp
        net = self.get_net()

        response.object_count = 0  # Initialize object_count

        for obj in self.mask_binaries:
            class_name, index, mask, cart = obj
            self.mask_binary = mask
            end_points, cloud = self.get_and_process_data()
            gg = self.infer_grasps(net, end_points)
            if cfgs.collision_thresh > 0:
                gg = self.collision_detection(gg, np.array(cloud.points))
            
            # -- Debug feature
            self.vis_grasps(gg)

            # Post-process and pick best grasp
            gg.nms()
            gg.sort_by_score()

            detected_object = DetectedObject()
            detected_object.name = f"{class_name} {index}"

            position_homogeneous = np.array([cart[0], cart[1], cart[2], 1.0])
            position_world_homogeneous = np.dot(self.transformation_matrix, position_homogeneous)

            detected_object.center_of_object = Point(x=np.round(position_world_homogeneous[0], 3), 
                                                     y=np.round(position_world_homogeneous[1], 3), 
                                                     z=np.round(position_world_homogeneous[2], 3))
            detected_object.grasps = []

            rotation_matrix = self.transformation_matrix[:3, :3]

            if len(gg) > 0:
                top_grasp = gg[0]

                # Create Grasp6D message for the top grasp
                grasp_msg = Grasp6D()

                # Make a cv2 image that showcases the grasp!
                grasp_cam_xyz = np.array(top_grasp.translation)
                x, y, z = grasp_cam_xyz

                fx, fy = self.intrinsic[0, 0], self.intrinsic[1, 1]
                cx, cy = self.intrinsic[0, 2], self.intrinsic[1, 2]

                u = int((x * fx / z) + cx)
                v = int((y * fy / z) + cy)

                # Draw grasp as a circle on the color image
                cv2.circle(self.cv2img, (u, v), radius=2, color=(0, 255, 0), thickness=2)

                # Extract position & orientation
                grasp_position_homogeneous = np.array([top_grasp.translation[0], top_grasp.translation[1], top_grasp.translation[2], 1.0])
                grasp_rotation_matrix = np.array(top_grasp.rotation_matrix).reshape(3, 3)
                
                # Draw the grasps on the image:
                line_offset = self.width / 2

                gripper_y_axis = grasp_rotation_matrix[:, 1]  # Y-axis of the gripper

                line_start_y = grasp_cam_xyz - line_offset * gripper_y_axis
                line_end_y = grasp_cam_xyz + line_offset * gripper_y_axis

                # Project the start and end points of the grasp width lines to 2D for Y-axis lines
                line_start_y_u = int((line_start_y[0] * fx / line_start_y[2]) + cx)
                line_start_y_v = int((line_start_y[1] * fy / line_start_y[2]) + cy)
                line_end_y_u = int((line_end_y[0] * fx / line_end_y[2]) + cx)
                line_end_y_v = int((line_end_y[1] * fy / line_end_y[2]) + cy)

                # Draw the Y-axis lines on the image (representing part of the grasp width)
                cv2.line(self.cv2img, (line_start_y_u, line_start_y_v), (line_end_y_u, line_end_y_v), (255, 0, 0), 3)

                # --- Approach direction line (Z-axis of gripper) ---
                approach_length = 0.05  # You can tune this value (in meters)
                gripper_z_axis = grasp_rotation_matrix[:, 2]

                approach_start = grasp_cam_xyz
                approach_end = grasp_cam_xyz + approach_length * gripper_z_axis

                approach_start_u = int((approach_start[0] * fx / approach_start[2]) + cx)
                approach_start_v = int((approach_start[1] * fy / approach_start[2]) + cy)
                approach_end_u = int((approach_end[0] * fx / approach_end[2]) + cx)
                approach_end_v = int((approach_end[1] * fy / approach_end[2]) + cy)

                cv2.line(self.cv2img, (approach_start_u, approach_start_v), (approach_end_u, approach_end_v), (0, 0, 255), 2)

                # Convert the image to a ROS message and publish
                image_msg = self.realsense_camera.bridge.cv2_to_imgmsg(self.cv2img.astype(np.uint8), encoding="rgb8")
                self.image_publisher.publish(image_msg)

                # Crop image and save it to PC, for test section!
                # Define crop boundaries
                crop_size = 100  # Half of 200
                h, w, _ = self.cv2img.shape

                # Ensure crop boundaries stay within image bounds
                x_min = max(u - crop_size, 0)
                y_min = max(v - crop_size, 0)
                x_max = min(u + crop_size, w)
                y_max = min(v + crop_size, h)

                # Crop the image
                cropped_img = self.cv2img[y_min:y_max, x_min:x_max]

                # Save to disk
                save_path = os.path.expanduser("~/Desktop/cropped_grasp_image.png")
                cv2.imwrite(save_path, cropped_img)

                # Change to world frame
                grasp_position_world_homogeneous = np.dot(self.transformation_matrix, grasp_position_homogeneous)

                grasp_msg.position = Point(
                    x=np.round(grasp_position_world_homogeneous[0], 3),
                    y=np.round(grasp_position_world_homogeneous[1], 3),
                    z=np.round(grasp_position_world_homogeneous[2], 3)
                )

                combined_rotation_matrix = np.dot(rotation_matrix, grasp_rotation_matrix)

                r = R.from_matrix(combined_rotation_matrix)
                roll, pitch, yaw = r.as_euler('xyz', degrees=True)

                # Wrap angles within +-180 degs, so 181 is -179, -190 is 170
                grasp_msg.orientation = Vector3(
                    x=(roll + 180) % 360 - 180,
                    y=(pitch + 180) % 360 - 180,
                    z=(yaw + 180) % 360 - 180
                )

                # Set grasp width
                grasp_msg.grasp_width = round(float(top_grasp.width), 3)

                # Append the grasp to the list of grasps
                detected_object.grasps.append(grasp_msg)

            # Fill the response
            response.detected_objects.append(detected_object)
            response.object_count += 1

        return response


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
        self.cv2img = cv2.cvtColor(self.color_frame, cv2.COLOR_RGB2BGR)
        self.color = self.color_frame / 255.0


    def get_object_information(self, request, response):
        det_object = request.object_name
        
        #Compute workspace_mask using YOLO & SAM
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes
        sam = SAM("sam_b.pt")

        model.set_classes([det_object])  # Set the class list to only include the specified object
            
        # Execute inference with the YOLOv8l-world model on the specified image
        yolo_results = model.predict(self.cv2img, verbose=False, conf=0.4, device='cuda:0') #, conf = 0.3

        # Sanity check - Was object detected?
        if len(yolo_results[0].boxes.data) > 0:
            self.mask_binaries = []
            for i in range(len(yolo_results[0].boxes.data)): # for each detected object it finds grasp poses
                box = yolo_results[0].boxes.data[i]
                x_min, y_min, x_max, y_max = box[:4]
                class_id = int(box[5])
                class_name = model.names[class_id]  # get class name

                # Getting the center coordinate to follow the format:
                pixel_x = int((x_min + x_max) / 2)
                pixel_y = int((y_min + y_max) / 2)

                # Extract camera intrinsic parameters
                fx = self.intrinsic[0, 0]
                fy = self.intrinsic[1, 1]
                cx = self.intrinsic[0, 2]
                cy = self.intrinsic[1, 2]

                depth_value = self.depth_frame[pixel_y, pixel_x]

                z = depth_value / 1000.0
                x = (pixel_x - cx) * z / fx  # X coordinate
                y = (pixel_y - cy) * z / fy  # Y coordinate

                cart_point = np.array([x, y, z])

                # Use SAM on image using YOLO bounding boxes.
                sam_results = sam.predict(self.cv2img, stream=False, bboxes=[x_min, y_min, x_max, y_max], points=None, labels=None)
                sam_masks = (sam_results[0].masks.data.cpu().numpy()*255).astype(np.uint8)
                
                #convert the mask to binary
                mask_binary = (sam_masks > 0).astype(np.uint8)
                mask_binary = np.squeeze(mask_binary)  # From shape (1, H, W) → (H, W)
                
                # Surface Normal Approximation to find highest graspable area:
                points_3d = []
                uvs = []
                for v in range(mask_binary.shape[0]):
                    for u in range(mask_binary.shape[1]):
                        if mask_binary[v, u]:
                            z = self.depth_frame[v, u] / 1000.0
                            if z == 0:
                                continue
                            x = (u - cx) * z / fx
                            y = (v - cy) * z / fy
                            points_3d.append([x, y, z])
                            uvs.append((u, v))

                points_3d = np.array(points_3d)
                pixel_coords = np.array(uvs)

                # Open3D point cloud & normal estimation
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(points_3d)
                pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(knn=30))

                # RANSAC Plane Segmentation (find dominant plane in region)
                plane_model, inliers = pcd.segment_plane(distance_threshold=0.10,
                                                        ransac_n=3,
                                                        num_iterations=1000)

                # Get inlier pixels (i.e., mask pixels belonging to the selected plane)
                inlier_pixels = pixel_coords[inliers]

                # Create filtered binary mask
                filtered_mask = np.zeros_like(mask_binary, dtype=np.uint8)
                for u, v in inlier_pixels:
                    if 0 <= v < filtered_mask.shape[0] and 0 <= u < filtered_mask.shape[1]:
                        filtered_mask[v, u] = 1

                self.mask_binaries.append([class_name, i, filtered_mask.astype(np.bool_), cart_point])
            return True
        else: # This is used to return a fail statement and a list of all objects in the workspace.
            model = YOLOWorld("yolov8l-world.pt")
            yolo_results = model.predict(self.cv2img, verbose=False, conf=0.4, device='cuda:0')
            self.objects_found = []
            for i in range(len(yolo_results[0].boxes.data)):
                self.objects_found.append(model.names[int(yolo_results[0].boxes.data[i][5])])

                # Publish image of the found objects
                image = yolo_results[0].plot()
                self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image))
            
            self.get_logger().info(f'YOLOWorld failed to detect {det_object}, but found {self.objects_found}')
            for i, name in enumerate(self.objects_found):
                obj = DetectedObject()
                obj.name = name
                
                box = yolo_results[0].boxes.data[i]
                x_min, y_min, x_max, y_max = box[:4]
                class_id = int(box[5])
                class_name = model.names[class_id]  # get class name

                # Getting the center coordinate to follow the format:
                pixel_x = int((x_min + x_max) / 2)
                pixel_y = int((y_min + y_max) / 2)

                # Extract camera intrinsic parameters
                fx = self.intrinsic[0, 0]
                fy = self.intrinsic[1, 1]
                cx = self.intrinsic[0, 2]
                cy = self.intrinsic[1, 2]

                depth_value = self.depth_frame[pixel_y, pixel_x]

                z = depth_value / 1000.0
                x = (pixel_x - cx) * z / fx  # X coordinate
                y = (pixel_y - cy) * z / fy  # Y coordinate

                cart_point = np.array([x, y, z])

                # Convert to homogeneous and use transformation matrix
                cart_point_hom = np.append(cart_point, 1.0) # Make homogeneous
                cart_point = self.transformation_matrix @ cart_point_hom 
                cart_point = cart_point[:3]  # Drop homogeneous coordinate

                # Fill in the message
                obj.center_of_object = Point(x=cart_point[0], y=cart_point[1], z=cart_point[2])
                obj.grasps = []  # No grasps since no object mask was found
                response.detected_objects.append(obj)
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
        
        # Set model to eval mode
        net.eval()
        return net

    def get_and_process_data(self):
        # generate cloud
        camera = CameraInfo(1280.0, 720.0, self.intrinsic[0][0], self.intrinsic[1][1], self.intrinsic[0][2], self.intrinsic[1][2], self.factor_depth)
        cloud_np = create_point_cloud_from_depth_image(self.depth_frame, camera, organized=True)

        # get valid points
        mask = (self.mask_binary & (self.depth_frame > 0))
        cloud_masked = cloud_np[mask]
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
        #cloud.points = o3d.utility.Vector3dVector(cloud_masked.astype(np.float32))
        cloud.colors = o3d.utility.Vector3dVector(color_masked.astype(np.float32))
        cloud_np = cloud_np.reshape(-1, 3)  # Flatten the cloud to shape (N, 3)

        cloud.points = o3d.utility.Vector3dVector(cloud_np.astype(np.float32)) # Changed to cloud
        #cloud.colors = o3d.utility.Vector3dVector(color.astype(np.float32)) # Changed to full img
        
        self.storage = o3d.geometry.PointCloud()
        self.storage.points = o3d.utility.Vector3dVector(cloud_masked.astype(np.float32))
        self.storage.colors = o3d.utility.Vector3dVector(color_masked.astype(np.float32))

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
        mfcdetector = ModelFreeCollisionDetector(cloud, voxel_size=cfgs.voxel_size, finger_width=0.03, finger_length=0.11)
        collision_mask = mfcdetector.detect(gg, approach_dist=0, collision_thresh=cfgs.collision_thresh)
        gg = gg[~collision_mask]
        return gg

    # No longer used, but debug feature for visualising grasp!
    def vis_grasps(self, gg):
        gg.nms()
        gg.sort_by_score()
        gg = gg[:1]
        grippers = gg.to_open3d_geometry_list()
        o3d.visualization.draw_geometries([self.storage, *grippers])


def main(args=None):
    rclpy.init(args=args)
    graspnetinstance = AnyGraspPipeline()
    rclpy.spin(graspnetinstance) 
    rclpy.shutdown()

if __name__=='__main__':
    main()
    