#Yolo World
from ultralytics import YOLOWorld    #pip install ultralytics

#SAM
from ultralytics import SAM
import torch

#Point cloud
import open3d as o3d
import sensor_msgs_py.point_cloud2 as pc2  # For converting PointCloud2 to numpy
from sklearn.decomposition import PCA
from scipy.spatial.transform import Rotation as ROT
from sklearn.cluster import DBSCAN
from collections import deque

#Image processing
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import os

# Simulation
from utils.mode_switch import load_use_sim

#ROS stuff
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import GetSimCameraData
from project_interfaces.msg import Grasp6D, DetectedObject, TransformMatrix
from geometry_msgs.msg import Point
from geometry_msgs.msg import Vector3 #for the 6D grasp prediction
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseArray



#the following is the ros2 launch command for the realsense camera with user settings
"""
ros2 launch realsense2_camera rs_launch.py 

IF THIS DOES NOT WORK, TRY THE FOLLOWING:
Check if secure boot is disabled in the BIOS or else it will not work!!!

If you want to chance any parameters do it in the launch file and remember to colcon build the package after you have made the changes.

"""

class RealSenseCamera(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')
        
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

         # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            CameraInfo,  # Message type
            '/camera/camera/aligned_depth_to_color/camera_info',  # Topic name
            self.camera_info_callback,  # Callback function
            10  # Queue size
        )
        
        self.subscription  # Prevent unused variable warning
        self.bridge = CvBridge()  

        #Image frames for depth and color
        self.color_img = None
        self.depth_img = None
        self.camera_info = None
        

        
    def convert_to_depth_img(self, msg):
        try:
            # Convert the ROS Image message to OpenCV image (16-bit single-channel)
            self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting image: {e}')

    def convert_to_color_img(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            color_img_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR by default)
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting color image: {e}')

        
    def camera_info_callback(self, msg):
        self.camera_info = msg.k


class SimCamera(Node):
    def __init__(self):
        super().__init__('sim_camera_node')
        self.bridge = CvBridge()

        self.color_img = None
        self.depth_img = None
        self.camera_info = None

        self.client = self.create_client(GetSimCameraData, 'get_simulated_camera_data')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for simulated camera data service...')

    def update_images(self):
        request = GetSimCameraData.Request()
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            response = future.result()

            # Convert image messages to OpenCV
            self.depth_img = self.bridge.imgmsg_to_cv2(response.depth_image, desired_encoding="16UC1")

            color_img_rgb = self.bridge.imgmsg_to_cv2(response.color_image, desired_encoding="rgb8")
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

            self.camera_info = response.camera_info.k
        else:
            self.get_logger().error("Failed to get simulated camera data")


""" 
In the grasp pipeline the following parameters are of importance: DO NOT CHANGE THEM UNLESS YOU KNOW WHAT YOU ARE DOING!!!! (Ask Signe, She doesent even know so dont touch them!!!!)
    - conf: Yolo World confidence threshold (currently not used so default(0.25))
    - num_candidates: The number of grasps candidates.
    - grasp_height: you chose how high you want the center point to be. for instance 0.25 places the center point 25% down from the highest point in the surface group.
    - clustered: If True, the mask is clustered using morphological operations. This is important for the grasp pose estimation as it removes information.
    - iterations: iterations for the morphological operations.
    - voxel_size: The size of the voxel grid for downsampling the point cloud. Smaller values retain more detail but increase computation time.
    - angle_threshold_deg: The maximum angle (in degrees) between normals to be considered similar.
    - distance_threshold: The maximum 3D distance to consider points as neighbors. This increases computation time.
    - k: The number of neighbors to consider for the mean filter. 
    - jump_threshold: The threshold for filtering out points with large depth jumps.
    
"""

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')

        self.camera_source = RealSenseCamera()

        self.detector_srv = self.create_service(GetObjectInfo, 'get_object_info', self.get_object_information)

        self.image_publisher = self.create_publisher(Image, 'video_frames', 10)

        # Instantiate the RealSenseCamera object
        self.realsense_camera = RealSenseCamera()

        # Create a dictionary to store found objects with relevant information
        self.found_objects = {}

        #Frames for depth and color
        self.depth_frame = None   
        self.color_frame = None
        self.camera_info = None

        #Point cloud
        self.point_cloud = None
        self.transformation_matrix = None
        
        #YOLO and SAM results
        self.yolo_results = None
        self.sam_result_img = None
        self.sam_masks = None

        # Publish initial image to GUI
        self.retrieve_aligned_frames()
        image = self.get_color_image()
        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image))


    def retrieve_aligned_frames(self):
        self.get_logger().error(f'{load_use_sim()}\n')
        if load_use_sim():
            self.get_logger().info(f'Using sim camera\n')
            sim_camera = SimCamera()
        
            sim_camera.update_images()

            self.get_logger().info(f'Get image\n')
    
            self.depth_frame = sim_camera.depth_img
            self.color_frame = sim_camera.color_img
            self.camera_info = sim_camera.camera_info
        else:
            self.get_logger().info(f'Using real camera\n')
            while self.realsense_camera.depth_img is None or self.realsense_camera.color_img is None or self.realsense_camera.camera_info is None:
                rclpy.spin_once(self.realsense_camera)

            while np.array_equal(self.realsense_camera.depth_img, self.depth_frame) or np.array_equal(self.realsense_camera.color_img, self.color_frame):
                rclpy.spin_once(self.realsense_camera)
            
            self.depth_frame = self.realsense_camera.depth_img
            self.color_frame = self.realsense_camera.color_img
            self.camera_info = self.realsense_camera.camera_info
         
    
    def create_point_cloud(self):
        # The camera info message .K contains the camera intrinsics
        #[ fx   0  cx ]
        #[  0  fy  cy ]
        #[  0   0   1 ]
        # Get the camera intrinsics
        fx = self.camera_info[0]
        fy = self.camera_info[4]
        cx = self.camera_info[2]
        cy = self.camera_info[5]

        height, width = self.depth_frame.shape

        # Create a grid of pixel coordinates (u, v)
        u, v = np.meshgrid(np.arange(width), np.arange(height))

        # Get the depth in meters
        z = self.depth_frame.astype(np.float32) / 1000.0  # Convert to meters

        # Replace 0.0 with np.nan to mark invalid pixels
        z[z == 0.0] = np.nan

        # Reproject to 3D space
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy

        # Stack into a (H, W, 3) point cloud
        self.point_cloud = np.stack((x, y, z), axis=-1) # organized point cloud (H, W, 3)

    
    #The callback function for the detector service for YOLO World
    def get_object_information(self, request, response, clustered = True):
        object = request.object_name
        self.get_logger().info(f'Requested to find {object}\n')

        self.found_objects.clear()
        self.transformation_matrix = np.array(request.transform.matrix).reshape((4, 4))  
        self.get_logger().info(f'Requested to find {object} with Yolo World\n')

        self.retrieve_aligned_frames()
        image = self.get_color_image()
        #image = cv2.rotate(image, cv2.ROTATE_180)

        self.get_logger().info(f"Image size: {image.shape}")

        #Apply Yolo World, data is stored in self.yolo_results
        self.apply_yolo_world(image, object, verbose=False)


        # If no objects are found with the specified class, try to find any object and return the class
        if len(self.yolo_results[0].boxes.data) == 0:
            self.get_logger().info(f'No {object} found\n')
            objects_found_list = self.apply_yolo_world(image, object, verbose=False, name_objects = True)
            image = self.yolo_results[0].plot()

            self.get_logger().info(f"Image size after plotting: {image.shape}")

            self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image))

            if False: 
                cv2.imshow("Yolo detections", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            response.object_count = 0

            for i, name in enumerate(objects_found_list):
                obj = DetectedObject()
                obj.name = name
                x_min, y_min, x_max, y_max, _ , _ = self.yolo_results[0].boxes.data[i]

                # Convert pixel coordinates to 3D coordinates
                cart_point = self.get_cartesian_coordinates(int((x_min + x_max) / 2), int((y_min + y_max) / 2))

                # Fill in the message
                obj.center_of_object = Point(x=cart_point[0], y=cart_point[1], z=cart_point[2])
                obj.grasps = []  # No grasps since no object mask was found
                response.detected_objects.append(obj)
            return response
        
        image_with_bbx = self.yolo_results[0].plot()

        self.get_logger().info(f'Found {len(self.yolo_results[0].boxes.data)} {object}\n')

        #self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image_with_bbx))

        if False:
            # Show the image with bounding boxes
            cv2.imshow("Image with Bounding Boxes", image_with_bbx)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.create_point_cloud()
        all_grasps = []


        for i in range(len(self.yolo_results[0].boxes.data)): # for each detected object it finds grasp poses
            x_min, y_min, x_max, y_max, _ , _ = self.yolo_results[0].boxes.data[i]  #_, _ = confidence and class
            self.get_logger().info(f'SAM segmenting bounding box.\n')
            self.SAM_predict(image, bboxes=[x_min, y_min, x_max, y_max], verbose=False) #updates sam_result_img and sam_masks
            torch.cuda.empty_cache() # Clear GPU memory TODO
            # checks if the mask size matches the point cloud size
            if self.sam_masks.shape[1] != self.point_cloud.shape[0]:
                self.get_logger().warn("Mask size doesn't match point cloud...")
                self.get_logger().warn(f"shapes: mask:{self.sam_masks.shape} vs pc: {self.point_cloud.shape}")
                continue
            
            #convert the mask to binary
            mask_binary = (self.sam_masks > 0).astype(np.uint8)
            mask_binary = np.squeeze(mask_binary)  # From shape (1, H, W) → (H, W)

            # Apply morphological operations to the mask 
            if clustered: #Performs morphological operations on the mask
                # Create a kernel for the morphological operation
                kernel = np.ones((5, 5), np.uint8)  # Adjust the size of the kernel to control how much the mask shrinks
                # Perform closing (dilate then erode)
                mask_closed = cv2.morphologyEx(mask_binary, cv2.MORPH_CLOSE, kernel)
                # Step 2: Shrink the mask using erosion
                mask_binary = cv2.erode(mask_closed, kernel, iterations = 4)  # You can adjust iterations for more shrinking
            
            # Visualize the mask
            if False: # Set to True to show the masks and the overlay
                # Remove the batch dimension
                overlay = cv2.addWeighted(self.color_frame, 0.7, cv2.cvtColor(mask_binary * 255, cv2.COLOR_GRAY2BGR), 0.3, 0)
                cv2.imshow("Overlayed Mask", overlay)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                
            #Apply the mask to the point cloud
            point_cloud_masked = self.point_cloud * mask_binary[..., np.newaxis]
            grasps = self.grasp_prediction(point_cloud_masked, num_candidates=1) # num_candidates is the number of grasps to be generated
            self.get_logger().info(f'Grasps found: {len(grasps)}\n')
            all_grasps.extend(grasps)


            detected_object = DetectedObject()
            detected_object.grasps = []

            # Find center of the object in 3D space
            x_min, y_min, x_max, y_max, _ , _ = self.yolo_results[0].boxes.data[i]
            # Convert pixel coordinates to 3D coordinates
            cart_point = self.get_cartesian_coordinates(int((x_min + x_max) / 2), int((y_min + y_max) / 2))
            # Fill in the message
            detected_object.center_of_object = Point(x=cart_point[0], y=cart_point[1], z=cart_point[2])
            detected_object.name = ( f"{object} {i}")
            detected_object.center_of_object

            for grasp in grasps:
                grasp_msg = Grasp6D()
                # Fill position
                grasp_msg.position = Point(x=grasp[0], y=grasp[1], z=grasp[2])
                # Fill orientation
                grasp_msg.orientation = Vector3(x=grasp[3], y=grasp[4], z=grasp[5])
                # Fill width
                grasp_msg.grasp_width = grasp[6] #grasp width
                detected_object.grasps.append(grasp_msg) 

            response.detected_objects.append(detected_object)
            response.object_count += 1

        if True:  # Visualize grasp lines on image
            image_copy = self.color_frame.copy()

            fx = self.camera_info[0]
            fy = self.camera_info[4]
            cx = self.camera_info[2]
            cy = self.camera_info[5]

            for grasp in all_grasps: 
                x, y, z, roll, pitch, yaw, grasp_witdh = grasp
                center = np.array([x, y, z])

                # Get rotation matrix from RPY
                # Convert orientation from degrees to radians
                roll, pitch, yaw = np.deg2rad([roll, pitch, yaw])
                rot = ROT.from_euler('xyz', [roll, pitch, yaw]).as_matrix()

                # Grasp opening direction (gripper x-axis)
                x_axis = rot[:, 0] * (grasp_witdh/2)  # 5 cm in opening direction
                # Approach direction (gripper -z)
                z_axis = -rot[:, 2] * 0.05  # 5 cm in approach direction

                # Define endpoints of lines
                grasp_left = center - x_axis
                grasp_right = center + x_axis
                handle = center + z_axis

                # Project points to image
                pt_left = self.project(grasp_left, fx, fy, cx, cy)
                pt_right = self.project(grasp_right, fx, fy, cx, cy)
                pt_handle = self.project(handle, fx, fy, cx, cy)
                pt_center = self.project(center, fx, fy, cx, cy)
                self.get_logger().info(f'Grasp left: {grasp_left}, Grasp right: {grasp_right}, Handle: {handle}, Center: {center}\n')
                self.get_logger().info(f'Projected points: {pt_left}, {pt_right}, {pt_handle}, {pt_center}\n')


                # Draw lines if all are valid
                if pt_left and pt_right:
                    cv2.line(image_copy, pt_left, pt_right, (0, 255, 0), 2)  # grasp line

                if pt_center and pt_handle:
                    cv2.line(image_copy, pt_center, pt_handle, (0, 0, 255), 2)  # approach dir
                
            self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image_copy))


        self.get_logger().info(f'Grasps found for {response.object_count} objects. Object detector Done.\n')
        return response

    def filter_by_depth_jump_np(self, pc_np, z_jump_threshold=0.04): #4 cm
        # Sort by depth (z-axis)
        sorted_indices = np.argsort(pc_np[:, 2])
        sorted_points = pc_np[sorted_indices]

        # Start with first point
        filtered_points = [sorted_points[0]]

        for i in range(1, len(sorted_points)):
            prev_z = sorted_points[i - 1, 2]
            curr_z = sorted_points[i, 2]

            # If the depth jump is small, keep the point
            if abs(curr_z - prev_z) <= z_jump_threshold:
                filtered_points.append(sorted_points[i])
            else:
                # Discontinuity detected — stop here
                break

        return np.array(filtered_points)

    def filter_by_depth_jump(self, pcd, jump_threshold=0.04):
        points_np = np.asarray(pcd)
        filtered_points = self.filter_by_depth_jump_np(points_np, jump_threshold)

        filtered_pcd = o3d.geometry.PointCloud()
        filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
        return filtered_pcd


    def SAM_predict(self, img, points = None, bboxes=None, labels = None, **kwargs):
        sam = SAM("sam_b.pt")

        # Stream True= you get predictions as they come, False = all at once better if realtime is not important!!
        # Labels define if a point is in the foreground[1] or background[0],
        # bboxes = [[x_min, y_min, x_max, y_max]]
        # points = [[x, y]] 
        # kwargs = can be additional arguments: mask_threshold=0.7, iou_threshold=0.5
        # info here: https://docs.ultralytics.com/reference/models/sam/model/#ultralytics.models.sam.model.SAM.info
        results = sam.predict(img, stream=False, bboxes=bboxes, points=points, labels=labels,**kwargs)
        
        # for plot(options)= https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Results.plot
        self.sam_result_img = results[0].plot(conf=True,
                                            line_width=None,
                                            font_size=None,
                                            labels=True,
                                            boxes=True,
                                            masks=True,
                                            probs=True) 
        
        # Publish the image to the GUI
        #self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(self.sam_result_img))
        
        # Convert all masks to NumPy and scale binary mask
        self.sam_masks = (results[0].masks.data.cpu().numpy()*255).astype(np.uint8)


    def segment_surfaces_by_normal_and_connectivity(self, pcd, angle_threshold_deg=10, distance_threshold=0.01, num_candidates=4):
        """
        Segments a point cloud into planar surface groups based on normal similarity and spatial connectivity.

        Args:
            pcd (o3d.geometry.PointCloud): Input point cloud with normals estimated.
            angle_threshold_deg (float): Max angle (in degrees) between normals to be considered similar.
            distance_threshold (float): Max 3D distance to consider points as neighbors. This increase computation time Points_total*r³=computations.
            num_candidates (int): Number of top surfaces to generate grasps for. 

        Returns:
            List[List[int]]: List of point index groups (each a list of indices).
        """
        normals = np.asarray(pcd.normals)
        points = np.asarray(pcd.points)
        used = np.zeros(len(points), dtype=bool)
        groups_all = []

        # Normalize angle threshold
        cos_thresh = np.cos(np.deg2rad(angle_threshold_deg))

        # Build KDTree for spatial neighbor search
        kdtree = o3d.geometry.KDTreeFlann(pcd)

        for seed_idx in range(len(points)):
            if used[seed_idx]:
                continue

            # Lock reference normal to the original seed point
            seed_normal = normals[seed_idx]

            queue = deque([seed_idx])
            used[seed_idx] = True
            group = [seed_idx]

            while queue:
                idx = queue.popleft()

                # Search spatial neighbors
                [_, neighbor_indices, _] = kdtree.search_radius_vector_3d(points[idx], distance_threshold)

                for ni in neighbor_indices:
                    if used[ni]:
                        continue

                    n_curr = normals[ni]
                    dot = np.dot(seed_normal, n_curr)

                    if dot > cos_thresh:
                        used[ni] = True
                        queue.append(ni)
                        group.append(ni)

            groups_all.append(group)
        
        #Take only the largest groups, sort groups by size (descending)
        sorted_groups = sorted(groups_all, key=lambda g: len(g), reverse=True)
        groups = sorted_groups[:num_candidates]

        if len(sorted_groups) < num_candidates:
            self.get_logger().info(f"Only found {len(sorted_groups)} groups, fewer than requested {num_candidates}")

        return groups

    def generate_grasp_candidates_from_groups(self, pcd, groups):
        """
        Generate grasp poses (6D) from the segmented surfaces.

        Args:
            pcd (o3d.geometry.PointCloud): Original point cloud (with normals).
            groups (List[List[int]]): List of index groups from segmentation.

        Returns:
            List[List[float]]: shape (len[groups], len[grasps]) grasp = [x, y, z, roll, pitch, yaw]
        """

        points = np.asarray(pcd.points)
        normals = np.asarray(pcd.normals)
        original_points = np.asarray(pcd.points)

        grasps = []

        # Generate a top-down grasp (approaching from above)
        if False: # Set to True to generate a top-down grasp
            top_grasp = self.generate_top_down_grasp(pcd)
            grasps.append(top_grasp) # dummy grasp

        for group in groups:
            surface_points = points[group]
            surface_normals = normals[group]

            # Estimate approach vector (mean normal)
            approach = -np.mean(surface_normals, axis=0)
            approach /= np.linalg.norm(approach)

            # PCA on surface points
            pca = PCA(n_components=3)
            pca.fit(surface_points)

            # Grasp position
            center = surface_points.mean(axis=0)

            
            if True: 
                # shift grasp center z value to grasp height
                if max(surface_points[:, 2]) - min(surface_points[:, 2]) > 0.02: # if the object is not flat
                    grasp_height = 0.25 # Controls how far up to grasp
                    z_min = np.min(surface_points[:, 2])
                    z_max = np.max(surface_points[:, 2])
                    center[2] = z_max - grasp_height * (z_max - z_min)

            # Opening direction = PCA component 1 (shorter in-plane axis)
            x_axis = pca.components_[1]


            y_axis = np.cross(approach, x_axis)

            # Re-orthonormalize (ensures that no numerical errors occur in the calculated rotation matrix and that they are orthognormal) 
            R_matrix = np.stack([x_axis, y_axis, approach], axis=1)
            U, _, Vt = np.linalg.svd(R_matrix)
            R_ortho = U @ Vt

            # Convert to roll-pitch-yaw
            rpy = ROT.from_matrix(R_ortho).as_euler('xyz', degrees=True)

            # calculate the grasp width based on the x-axis and the plane it spans and the original point cloud
            plane_normal = approach
            plane_point = center

            #  Filter points near the x-y plane (with threshold)
            distances_to_plane = np.abs((original_points - plane_point) @ plane_normal)
            on_plane_mask = distances_to_plane < 0.005  # 0.5 cm

            plane_points = original_points[on_plane_mask]

            if len(plane_points) < 2:
                grasp_width = 0.15  # Not enough data so max width
            else:
                # Project points onto x-axis to get scalar positions along grasp width direction
                projections = (plane_points - center) @ x_axis
                min_proj = np.min(projections)
                max_proj = np.max(projections)

                grasp_width = np.abs(max_proj - min_proj)

            # Add grasp to list [x, y, z, roll, pitch, yaw]
            grasps.append([float(center[0]), float(center[1]), float(center[2]), float(rpy[0]), float(rpy[1]), float(rpy[2]), float(grasp_width)])

        return grasps

    def invert_transformation_matrix(self, T):
            """
            Inverts a 4x4 transformation matrix.
            """
            R = T[:3, :3]
            t = T[:3, 3]
            R_inv = R.T
            t_inv = -np.dot(R_inv, t)
            T_inv = np.eye(4)
            T_inv[:3, :3] = R_inv
            T_inv[:3, 3] = t_inv
            return T_inv


    def grasp_prediction(self, point_cloud_masked, num_candidates):
        ################################################################
                # Filter the point cloud
        ################################################################

        #reformatting (H, W, 3) to (N, 3)
        pc_np = point_cloud_masked.reshape(-1, 3)
        # Filter out points with NaNs or zero depth (z <= 0)
        valid = ~np.isnan(pc_np).any(axis=1) & (pc_np[:, 2] > 0)
        pc_np_filtered = pc_np[valid]
        # Filter out points with large depth jumps to remove noise
        pc_np_filtered = self.filter_by_depth_jump_np(pc_np_filtered) 
        
        # Sanity check
        if len(pc_np_filtered) == 0:
            self.get_logger().info("No valid points in masked point cloud.")
            return
    
        ################################################################
                # Create Open3D point cloud, downsample, tranform, and estimate normals
        ################################################################

        # Create Open3D point cloud
        pcd = o3d.geometry.PointCloud() #point cloud object
        pcd.points = o3d.utility.Vector3dVector(pc_np_filtered)

        if len(pcd.points) > 20000:
            # Downsample the point cloud into 1 mm cubes
            pcd = pcd.voxel_down_sample(voxel_size=0.001) # 1 mm cubes

        # filter out points with large depth jumps as voxel downsampling can create noise
        pcd = self.filter_by_depth_jump(pcd.points, jump_threshold=0.02) 

        if True: #True: transform the point cloud to the global frame TODO
            # transform the point cloud from local to global frame
            pcd = self.transform_pointcloud_to_global(pcd, self.transformation_matrix)

        if True: #True: apply mean filter to smothe the point cloud - this improves surface estimation
            pcd = self.knn_mean_filter(pcd, k=30) # tuning of k is important and does greatly affect the result

        # Estimate normals
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=30))

        #orient normals consistently. Important for surface estimation !!!
        try:
            pcd.orient_normals_consistent_tangent_plane(k=30) # k is the number of neighbors to consider
        except RuntimeError:
            camera_location_global = (self.transformation_matrix @ np.array([0, 0, 0, 1]))[:3] 
            pcd.orient_normals_towards_camera_location(camera_location_global)
            self.get_logger().info("Points to flat for orienting normals using tangent plane. Instead using camera location to orient normals.")


        ################################################################
        # Estimate surfaces and grasps 
        ################################################################

        # Estimate surfaces based on normal similarity and spatial connectivity
        groups = self.segment_surfaces_by_normal_and_connectivity(pcd, angle_threshold_deg=20, distance_threshold=0.01, num_candidates=num_candidates)
        # Generate grasp candidates from the segmented surfaces. Outputs a list of grasps
        grasps = self.generate_grasp_candidates_from_groups(pcd, groups)

        ################################################################
        # Visualize result
        ################################################################

        if False: # Set to True to visualize the point cloud and grasp poses
            # Visualize the camera frame
            camera_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.01)

            # Creating the grasp frames       
            grasp_frames = []
            for grasp in grasps:
                x, y, z, roll, pitch, yaw = grasp

                # Convert RPY to rotation matrix
                rot = ROT.from_euler('xyz', [roll, pitch, yaw]).as_matrix()

                # Create coordinate frame and apply transform
                frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.025)
                frame.rotate(rot, center=(0, 0, 0))
                frame.translate([x, y, z])

                grasp_frames.append(frame)

            # Make point cloud blue
            pcd.paint_uniform_color([0, 0, 1]) # blue

            # you can visualise: camera_frame, pcd, grasp_frames, normals
            o3d.visualization.draw_geometries([pcd,*grasp_frames], point_show_normal=False, window_name="Grasp Poses", width=800, height=600)
        
        ################################################################
        # :Return the grasp pose
        ################################################################
        return grasps

    def project(self, pt3d, fx, fy, cx, cy):
                x, y, z = pt3d
                if z <= 0:
                    return None
                u = int((x * fx / z) + cx)
                v = int((y * fy / z) + cy)
                return (u, v)
    

    def generate_top_down_grasp(self, global_pointcloud, top_band_height=0.005):
        """
        Generate a grasp that approaches from the top (negative Z).
        
        Args:
            original_pointcloud (np.ndarray): Nx3 array of 3D points in global frame.
            top_band_height (float): Thickness (in meters) of top layer to consider.

        Returns:
            List[float]: [x, y, z, roll, pitch, yaw, width] of the grasp.
        """
        # Convert to numpy array
        global_pointcloud = np.asarray(global_pointcloud.points)

        # Filter out invalid points
        valid = ~np.isnan(global_pointcloud).any(axis=1)
        pc = global_pointcloud[valid]

        if pc.shape[0] == 0:
            print("No valid points in point cloud.")
            return None

        # Sort by Z (height)
        pc_sorted = pc[np.argsort(pc[:, 2])] 

        # Get the highest z value
        z_max = pc_sorted[-1, 2]

        # Select points within top_band_height of max height
        top_points = pc_sorted[pc_sorted[:, 2] > (z_max - top_band_height)]

        # Compute center of top surface
        center = np.mean(top_points, axis=0)

        # Orientation:
        # Approach from top → -Z axis
        # X and Y are found using PCA 
        # PCA on surface points
        approach = np.array([0, 0, -1])  # approach direction (down)

        pca = PCA(n_components=3)
        pca.fit(top_points)

        # Opening direction = PCA component 1 (shorter in-plane axis)
        x_axis = pca.components_[1]
        y_axis = np.cross(approach, x_axis)

        # Re-orthonormalize (ensures that no numerical errors occur in the calculated rotation matrix and that they are orthognormal) 
        R_matrix = np.stack([x_axis, y_axis, approach], axis=1)
        U, _, Vt = np.linalg.svd(R_matrix)
        R_ortho = U @ Vt


        # Convert to roll-pitch-yaw
        rpy = ROT.from_matrix(R_ortho).as_euler('xyz', degrees=True)

        # calculate the grasp width based on the x-axis and the plane it spans and the original point cloud
        plane_normal = approach
        plane_point = center

        #  Filter points near the x-y plane (with threshold)
        distances_to_plane = np.abs((global_pointcloud - plane_point) @ plane_normal)
        on_plane_mask = distances_to_plane < top_band_height  # 0.5 cm

        plane_points = global_pointcloud[on_plane_mask]

        if len(plane_points) < 2:
            grasp_width = 0.15  # Not enough data so max width
        else:
            # Project points onto x-axis to get scalar positions along grasp width direction
            projections = (plane_points - center) @ x_axis
            min_proj = np.min(projections)
            max_proj = np.max(projections)

            grasp_width = np.abs(max_proj - min_proj)

        # Return 6D pose with width
        return [*center, *rpy, float(grasp_width)]
    
    def transform_pointcloud_to_global(self, pointcloud, transformation_matrix):
        """
        Transforms a point cloud using a 4x4 transformation matrix.
        
        Args:
            pcd (o3d.geometry.PointCloud): Original point cloud
            transformation_matrix (np.ndarray): 4x4 transformation matrix.
        
        Returns:
            pcd (o3d.geometry.PointCloud): Transformed point cloud
        """
        pointcloud = np.asarray(pointcloud.points)
        if pointcloud.shape[1] != 3:
            raise ValueError("Point cloud must be Nx3")

        # Convert to homogeneous coordinates (Nx4)
        ones = np.ones((pointcloud.shape[0], 1))
        pc_homogeneous = np.hstack([pointcloud, ones])  # Nx4

        # Apply transformation
        pc_transformed = (transformation_matrix @ pc_homogeneous.T).T[:, :3]  # Nx3

        # Create new Open3D point cloud and assign points
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pc_transformed)
        
        return pcd


    def knn_mean_filter(self, pcd: o3d.geometry.PointCloud, k: int = 20) -> o3d.geometry.PointCloud:
        points = np.asarray(pcd.points)
        tree = o3d.geometry.KDTreeFlann(pcd)

        smoothed_points = []

        for i in range(len(points)):
            _, idx, _ = tree.search_knn_vector_3d(pcd.points[i], k)
            neighbor_points = points[idx]
            mean = neighbor_points.mean(axis=0)
            smoothed_points.append(mean)

        new_pcd = o3d.geometry.PointCloud()
        new_pcd.points = o3d.utility.Vector3dVector(np.array(smoothed_points))

        # Optionally keep normals if they exist and you want to smooth them too
        if pcd.has_normals():
            normals = np.asarray(pcd.normals)
            smoothed_normals = []
            for i in range(len(normals)):
                _, idx, _ = tree.search_knn_vector_3d(pcd.points[i], k)
                neighbor_normals = normals[idx]
                mean_n = neighbor_normals.mean(axis=0)
                mean_n /= np.linalg.norm(mean_n) + 1e-8  # normalize
                smoothed_normals.append(mean_n)
            new_pcd.normals = o3d.utility.Vector3dVector(np.array(smoothed_normals))

        return new_pcd


    def show_depth_map(self):
        cv2.namedWindow("Depth Map", cv2.WINDOW_AUTOSIZE)

        while True:
            self.retrieve_aligned_frames()

            # Convert the depth frame to a NumPy array
            depth_image = np.asanyarray(self.depth_frame)

            #depth_image = cv2.rotate(depth_image, cv2.ROTATE_180)

            if True: #True: gets a tresholded colormap. False all depth data are used in normalisation
                # Define the depth range (in millimeters) to display
                min_depth = 0  # Minimum depth to display  0 m
                max_depth = 3000  # Maximum depth to display 3m

                # 1. Threshold the depth image to the specified range
                # Set values outside the range to 0 (this can be chanced if needed).
                depth_image = np.where((depth_image >= min_depth) & (depth_image <= max_depth),depth_image, 0)

            # Normalize the depth image for display
            depth_image = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = np.uint8(depth_image)

            # Apply a colormap to the depth image
            depth_colormap = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # Show the depth map using OpenCV's imshow
            cv2.imshow("Depth Map", depth_colormap)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        cv2.destroyAllWindows()
        
    def show_frame(self):
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        while True:
            self.retrieve_aligned_frames()

            # Convert the frame to a NumPy array for OpenCV
            color_frame = self.get_color_image()

            # Show the frame using OpenCV's imshow
            cv2.imshow("Image", cv2.rotate(color_frame, cv2.ROTATE_180))

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def get_color_image(self):
        return np.asanyarray(self.color_frame)

    def show_image(self, image):
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def apply_yolo_world(self, img, object_name, name_objects = False, verbose = False):
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes
        
        if name_objects == False:
            model.set_classes([object_name])  # Set the class list to only include the specified object
            
        # Execute inference with the YOLOv8l-world model on the specified image
        self.yolo_results = model.predict(img, verbose=False) #, conf = 0.3

        #the following prints the results of the yolo model without the class contrains
        if name_objects:
            objects_found = []
            for i in range(len(self.yolo_results[0].boxes.data)):
                objects_found.append(model.names[int(self.yolo_results[0].boxes.data[i][5])])

            self.get_logger().info(f'No {object_name} were found, but {objects_found} was located.\n')
            return objects_found

    

    def get_cartesian_coordinates(self, pixel_x, pixel_y):
        # The camera info message .K contains the camera intrinsics
        #[ fx   0  cx ]
        #[  0  fy  cy ]
        #[  0   0   1 ]

        # Get the camera intrinsics
        fx = self.camera_info[0]
        fy = self.camera_info[4]
        cx = self.camera_info[2]
        cy = self.camera_info[5]

        self.get_logger().info(f"Depth frame size: {self.depth_frame.shape}")

        if pixel_x < 0 or pixel_x >= self.depth_frame.shape[1] or pixel_y < 0 or pixel_y >= self.depth_frame.shape[0]:
            self.get_logger().info(f"Pixel coordinates out of bounds: ({pixel_x}, {pixel_y})")
            return None
        
        if self.depth_frame[pixel_y, pixel_x] == 0:
            self.get_logger().info(f"No depth data available at the selected pixel: ({pixel_x}, {pixel_y})")
            return None

        # Calculate the x, y, z coordinates
        if load_use_sim():
            z = self.depth_frame[pixel_y, pixel_x] 
        else:
            z = self.depth_frame[pixel_y, pixel_x] / 1000  # Convert to meters

        x = ((pixel_x - cx) * z / fx) 
        y = ((pixel_y - cy) * z / fy) 
        

        return np.array([x, y, z])
        
    def show_cartesian_coordinates(self):
        self.retrieve_aligned_frames()
        color_image = self.get_color_image()

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                # Adjust the x, y coordinates to reflect a rotated image
                height, width, _ = color_image.shape
                adjusted_x = width - x
                adjusted_y = height - y
                coordinates = self.get_cartesian_coordinates(adjusted_x, adjusted_y)
                if coordinates is not None:
                    print(f"Cartesian coordinates at ({x}, {y}): {coordinates}")

        cv2.namedWindow("Image with Coordinates")
        cv2.setMouseCallback("Image with Coordinates", mouse_callback)

    
        while True:
            cv2.imshow("Image with Coordinates", cv2.rotate(color_image, cv2.ROTATE_180))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()



    def get_user_input(self, prompt):
        """
        Use console input instead of GUI input for simplicity.
        """
        while True:
            try:
                user_input = int(input(prompt))
                return user_input
            except ValueError:
                print("Invalid input. Please enter a number.")

    def save_image(self, save_folder="captured_images"):
        """
        Captures and saves an image in a specified folder with an incremented filename.
        """
        # Ensure the save folder exists
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Retrieve the current frame
        self.retrieve_aligned_frames()
        image = self.get_color_image()

        if image is None:
            print("Failed to capture image from camera.")
            return

        # Find the next available file name
        existing_files = [f for f in os.listdir(save_folder) if f.endswith(".jpg")]
        next_index = len(existing_files) + 1
        file_name = f"image_{next_index}.jpg"
        file_path = os.path.join(save_folder, file_name)

        # Save the image
        cv2.imwrite(file_path, image)  # Rotate if needed
        print(f"Image saved: {file_path}")


def main(args=None):
    rclpy.init(args=args)

    # Create an ObjectDetector instance
    detector = ObjectDetector()

    #this was commented out
    rclpy.spin(detector) 

    rclpy.shutdown()


if __name__ == '__main__':
    main()
