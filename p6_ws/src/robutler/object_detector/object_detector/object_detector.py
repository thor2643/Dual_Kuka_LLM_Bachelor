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
        self.get_logger().info("[SimCamera] Finished waiting for future")

        if future.result() is not None:
            response = future.result()

            # Convert image messages to OpenCV
            #self.depth_img = self.bridge.imgmsg_to_cv2(response.depth_image, desired_encoding="16UC1")
            self.depth_img = self.bridge.imgmsg_to_cv2(response.depth_image, desired_encoding="32FC1")

            color_img_rgb = self.bridge.imgmsg_to_cv2(response.color_image, desired_encoding="rgb8")
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

            self.camera_info = response.camera_info.k

            self.get_logger().info(f"[SimCamera] Depth image shape: {self.depth_img.shape}")
            self.get_logger().info(f"[SimCamera] Depth image min: {np.min(self.depth_img)}, max: {np.max(self.depth_img)}")
            self.get_logger().info(f"[SimCamera] Camera intrinsics: {self.camera_info}")

        else:
            self.get_logger().error("Failed to get simulated camera data")


"""     #### PARAMETERS FOR GRASP PREDICTION ####
In the grasp pipeline the following parameters are of importance: DO NOT CHANGE THEM UNLESS YOU KNOW WHAT YOU ARE DOING!!!! (Ask Signe)
    - confi: Yolo World confidence threshold 
    - num_candidates: The number of grasps candidates.
    - grasp_height: you chose how high you want the center point to be. for instance 0.25 places the center point 25% down from the highest point in the surface group.
    - clustered: If True, the mask is reduced using morphological operations. This is important if its clustered as it avoids noise in point cloud.
    - iterations: iterations for the morphological operations. How many times the mask is eroded.
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
        self.generate_general_grasp = False
        
        #YOLO and SAM results
        self.yolo_results = None
        self.sam_result_img = None
        self.sam_mask = None

        # Publish initial image to GUI
        self.retrieve_aligned_frames()
        image = self.get_color_image()
        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image))


    def retrieve_aligned_frames(self):
        self.get_logger().error(f'load_use_sim = {load_use_sim()}\n')
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
        if load_use_sim():
            z = self.depth_frame.astype(np.float32) # Convert to meters
        else:
            z = self.depth_frame.astype(np.float32) / 1000

        # Replace 0.0 with np.nan to mark invalid pixels
        z[z == 0.0] = np.nan

        # Reproject to 3D space
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy

        # Stack into a (H, W, 3) point cloud
        self.point_cloud = np.stack((x, y, z), axis=-1) # organized point cloud (H, W, 3)

    def get_click_location(self, image, object_name):
        coords = []
        self.get_logger().info(f"Click on object/objects: ({object_name}) (press 'q' to finish)...")

        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                coords.append((x, y))
                self.get_logger().info(f"Clicked at: ({x}, {y})")

        cv2.namedWindow(f"Click on object/objects: {object_name} (press 'q' to finish).")
        cv2.setMouseCallback(f"Click on object/objects: {object_name} (press 'q' to finish).", click_event)

        while True:
            temp_img = image.copy()
            # Optional: draw circles for all clicked points
            for (x, y) in coords:
                cv2.circle(temp_img, (x, y), 5, (0, 255, 0), -1)

            cv2.imshow(f"Click on object/objects: {object_name} (press 'q' to finish).", temp_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        if not coords:
            self.get_logger().warn("No points were selected.")

        return coords


    def apply_yolo_world(self, img, object_name, confi, name_objects = False, verbose = False):
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes
        
        if name_objects == False:
            model.set_classes([object_name])  # Set the class list to only include the specified object
            
        # Execute inference with the YOLOv8l-world model on the specified image
        self.yolo_results = model.predict(img, verbose=False, conf=confi)

        #the following prints the results of the yolo model without the class contrains
        if name_objects:
            objects_found = []
            for i in range(len(self.yolo_results[0].boxes.data)):
                objects_found.append(model.names[int(self.yolo_results[0].boxes.data[i][5])])

            self.get_logger().info(f'No {object_name} were found, but {objects_found} was located.\n')
            return objects_found

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
        self.sam_mask = (results[0].masks.data.cpu().numpy()*255).astype(np.uint8)

    
    #The callback function for the detector service for YOLO World
    def get_object_information(self, request, response, clustered = True):
        object = request.object_name
        self.get_logger().info(f'Requested to find {object}\n')

        self.found_objects.clear()
        self.transformation_matrix = np.array(request.transform.matrix).reshape((4, 4))  
        self.get_logger().info(f'Requested to find {object} with Yolo World\n')

        self.retrieve_aligned_frames()
        image = self.get_color_image()

        #Apply Yolo World, data is stored in self.yolo_results
        self.apply_yolo_world(image, object, confi = 0.15, verbose=False) #TODO afjust conf here

        self.create_point_cloud()
        all_grasps = []

        # If no objects are found with the specified class, try to find any object and return the class
        if len(self.yolo_results[0].boxes.data) == 0:
            cordinate_list = self.get_click_location(image, object)
            self.get_logger().info(f'Yolo did not find the object, User clicked instead.\n')
            for i, cords in enumerate(cordinate_list):  
                x, y = cords[0], cords[1]
                self.get_logger().info(f'SAM segmenting bounding box for object: {object}.\n')
                self.SAM_predict(image, points=[x,y], verbose=False) #updates sam_result_img and sam_masks
                torch.cuda.empty_cache() # Clear GPU memory 
                                    
                mask_binary = (self.sam_mask > 0).astype(np.uint8) #convert the mask to binary
                mask_binary = np.squeeze(mask_binary)  # From shape (1, H, W) → (H, W)

                size_pixel = np.count_nonzero(mask_binary)

                if size_pixel < 4000: # for example, if fewer than 20 pixels are lit
                    clustered = False
                else:
                    clustered = True

                # Apply morphological operations to the mask 
                if clustered: #Performs morphological operations on the mask
                    # Create a kernel for the morphological operation
                    kernel = np.ones((5, 5), np.uint8)  # Adjust the size of the kernel to control how much the mask shrinks
                    # Perform closing (dilate then erode)
                    mask_closed = cv2.morphologyEx(mask_binary, cv2.MORPH_CLOSE, kernel)
                    # Step 2: Shrink the mask using erosion
                    mask_binary = cv2.erode(mask_closed, kernel, iterations = 2)  # TODO was 4 before You can adjust iterations for more shrinking
                
                # Visualize the mask
                overlay = cv2.addWeighted(self.color_frame, 0.7, cv2.cvtColor(mask_binary * 255, cv2.COLOR_GRAY2BGR), 0.3, 0)
                self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(overlay))
                    
                #Apply the mask to the point cloud
                point_cloud_masked = self.point_cloud * mask_binary[..., np.newaxis]
                z_values = point_cloud_masked[mask_binary > 0, 2]
                mean_depth = np.mean(z_values[(z_values > 0) & (~np.isnan(z_values))])
                size_object = size_pixel * (mean_depth**2/(self.camera_info[0]*self.camera_info[4]))
                grasps = self.grasp_prediction(point_cloud_masked, num_candidates=1) # num_candidates is the number of grasps to be generated
                all_grasps.extend(grasps)

                detected_object = DetectedObject()
                detected_object.grasps = []

                # Find center of the object in 3D space
                x_min, y_min, x_max, y_max, _ , _ = x, y, x+2, y+2, 0 , 0
                # Convert pixel coordinates to 3D coordinates
                cart_point = self.get_cartesian_coordinates(int((x_min + x_max) / 2), int((y_min + y_max) / 2))
                if cart_point is None or len(cart_point) != 3:
                    self.get_logger().warn("Invalid cart_point, skipping transformation.")
                    continue
                    
                # Convert to homogeneous (4D)
                cart_point_hom = np.append(cart_point, 1.0) # Make homogeneous
                cart_point = self.transformation_matrix @ cart_point_hom 
                cart_point = cart_point[:3]  # Drop homogeneous coordinate
                
                # Fill in the message
                detected_object.center_of_object = Point(x=cart_point[0], y=cart_point[1], z=cart_point[2])
                detected_object.name = ( f"{object} {i+1}")
                detected_object.center_of_object
                detected_object.size_area = size_object

                for grasp in grasps:
                    if not grasp or len(grasp) < 6:
                        continue

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

        else: 
            for i in range(len(self.yolo_results[0].boxes.data)): # for each detected object it finds grasp poses
                x_min, y_min, x_max, y_max, confif , _ = self.yolo_results[0].boxes.data[i]  #_, _ = confidence and class
                self.get_logger().info(f'SAM segmenting bounding box for object {i+1}. conf: {round(confif.item(),2)}.\n')
                self.SAM_predict(image, bboxes=[x_min, y_min, x_max, y_max], verbose=False) #updates sam_result_img and sam_masks
                torch.cuda.empty_cache() # Clear GPU memory 

                #convert the mask to binary
                mask_binary = (self.sam_mask > 0).astype(np.uint8)
                mask_binary = np.squeeze(mask_binary)  # From shape (1, H, W) → (H, W)

                size_pixel = np.count_nonzero(mask_binary)

                if size_pixel < 4000:  # for example, if fewer than 20 pixels are lit
                    clustered = False
                else:
                    clustered = True

                # Apply morphological operations to the mask 
                if clustered: #Performs morphological operations on the mask
                    # Create a kernel for the morphological operation
                    kernel = np.ones((5, 5), np.uint8)  # Adjust the size of the kernel to control how much the mask shrinks
                    # Perform closing (dilate then erode)
                    mask_closed = cv2.morphologyEx(mask_binary, cv2.MORPH_CLOSE, kernel)
                    # Step 2: Shrink the mask using erosion
                    mask_binary = cv2.erode(mask_closed, kernel, iterations = 2)  # TODO was 4 before You can adjust iterations for more shrinking
                
                # Visualize the mask
                overlay = cv2.addWeighted(self.color_frame, 0.7, cv2.cvtColor(mask_binary * 255, cv2.COLOR_GRAY2BGR), 0.3, 0)
                self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(overlay))

                #Apply the mask to the point cloud
                point_cloud_masked = self.point_cloud * mask_binary[..., np.newaxis]
                z_values = point_cloud_masked[mask_binary > 0, 2]
                mean_depth = np.mean(z_values[(z_values > 0) & (~np.isnan(z_values))])
                size_object = size_pixel * (mean_depth**2/(self.camera_info[0]*self.camera_info[4]))
                grasps = self.grasp_prediction(point_cloud_masked, num_candidates=1) # num_candidates is the number of grasps to be generated
                all_grasps.extend(grasps)

                detected_object = DetectedObject()
                detected_object.grasps = []

                # Find center of the object in 3D space
                x_min, y_min, x_max, y_max, _ , _ = self.yolo_results[0].boxes.data[i]
                # Convert pixel coordinates to 3D coordinates
                cart_point = self.get_cartesian_coordinates(int((x_min + x_max) / 2), int((y_min + y_max) / 2))
                if cart_point is None or len(cart_point) != 3:
                        self.get_logger().warn("Invalid cart_point, skipping transformation.")
                        continue
                # Convert to homogeneous (4D)
                cart_point_hom = np.append(cart_point, 1.0) # Make homogeneous
                cart_point = self.transformation_matrix @ cart_point_hom 
                cart_point = cart_point[:3]  # Drop homogeneous coordinate

                # Fill in the message
                detected_object.center_of_object = Point(x=cart_point[0], y=cart_point[1], z=cart_point[2])
                detected_object.name = ( f"{object} {i+1}")
                detected_object.center_of_object
                detected_object.size_area = size_object

                for grasp in grasps:
                    if not grasp or len(grasp) < 6:
                        continue

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

        # Visualize grasp lines on image
        image_copy = self.color_frame.copy()
        T_C_W = self.invert_transformation_matrix(self.transformation_matrix)

        for grasp in all_grasps:           
            x, y, z, roll, pitch, yaw, grasp_width = grasp

            if z < 0 or grasp_width >= 0.1525:
                continue
            
            T_W_G = np.eye(4)
            T_W_G[:3, :3] = ROT.from_euler('xyz', [roll, pitch, yaw], degrees=True).as_matrix()
            T_W_G[:3, 3] = [x, y, z]

            # Now apply full transformation into camera frame
            T_C_G = T_C_W @ T_W_G
            center_cam = T_C_G[:3, 3]
            R_C_G = T_C_G[:3, :3]

            # Axes in camera frame
            x_axis_cam = R_C_G[:, 0] * (grasp_width / 2)
            z_axis_cam = -R_C_G[:, 2] * 0.05  # Approach direction

            to_camera_vec = -center_cam
            dot = np.dot(z_axis_cam, to_camera_vec)

            if dot < 0:
                z_axis_cam *= -1


            # Endpoints in camera frame
            grasp_left = center_cam - x_axis_cam
            grasp_right = center_cam + x_axis_cam
            handle = center_cam + z_axis_cam

            # Project to 2D
            pt_left = self.project(grasp_left)
            pt_right = self.project(grasp_right)
            pt_center = self.project(center_cam)
            pt_handle = self.project(handle)

            # Draw lines
            if pt_left and pt_center:
                cv2.line(image_copy, pt_left, pt_center, (0, 255, 0), 2)  # -X (green)
            if pt_right and pt_center:
                cv2.line(image_copy, pt_right, pt_center, (0, 0, 255), 2)  # +X (red)
            if pt_handle and pt_center:
                cv2.line(image_copy, pt_center, pt_handle, (255, 0, 0), 2)  # -Z (blue, approach)
            
        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image_copy))
        self.get_logger().info(f'Grasps found for {response.object_count} objects. Object detector Done.\n')
        return response
    
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

        # transform the point cloud from local to global frame
        pcd = self.transform_pointcloud_to_global(pcd, self.transformation_matrix)

        #apply mean filter to smothe the point cloud - this improves surface estimation
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
        groups = self.segment_surfaces_by_normal_and_connectivity(pcd, angle_threshold_deg=20, distance_threshold=0.01)
        # Generate grasp candidates from the segmented surfaces. Outputs a list of grasps
        grasps = self.generate_grasp_candidates_from_groups(pcd, groups, num_candidates)

        return grasps

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
    
    def transform_point(self, pt, T):
        pt_hom = np.append(pt, 1)  # Make homogeneous
        return (T @ pt_hom)[:3]    # Transform and drop homogeneous coord


    def segment_surfaces_by_normal_and_connectivity(self, pcd, angle_threshold_deg=10, distance_threshold=0.01):
        """
        Segments a point cloud into planar surface groups based on normal similarity and spatial connectivity.

        Args:
            pcd (o3d.geometry.PointCloud): Input point cloud with normals estimated.
            angle_threshold_deg (float): Max angle (in degrees) between normals to be considered similar.
            distance_threshold (float): Max 3D distance to consider points as neighbors. This increase computation time Points_total*r³=computations.

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
        groups = sorted(groups_all, key=lambda g: len(g), reverse=True)

        # Filter out small groups (keep only groups with at least 10 points)
        min_group_size = 10
        groups = [g for g in groups if len(g) >= min_group_size]
        
        return groups

    def generate_grasp_candidates_from_groups(self, pcd, groups, num_candidates):
        """
        Generate grasp poses (6D) from the segmented surfaces.

        Args:
            pcd (o3d.geometry.PointCloud): Original point cloud (with normals).
            groups (List[List[int]]): List of index groups from segmentation.
            num_candidates (int): Number of grasp candidates to generate.

        Returns:
            List[List[float]]: shape (len[groups], len[grasps]) grasp = [x, y, z, roll, pitch, yaw]
        """

        points = np.asarray(pcd.points)
        normals = np.asarray(pcd.normals)
        original_points = np.asarray(pcd.points)

        grasps = []
        count = 0 # valid grasp counter

        # create top_down grasp
        for idx, group in enumerate(groups):
            surface_normals = normals[group]
            
            # Estimate approach vector (mean normal)
            mean_normal = np.mean(surface_normals, axis=0)
            mean_normal /= np.linalg.norm(mean_normal)  # Normalize

            # Check if mean normal is close to (0,0,1)
            if np.dot(mean_normal, np.array([0, 0, 1])) > 0.95: # ca 18 degrees 
                surface_points = points[group]
                # Estimate approach vector (mean normal)
                approach = np.array([0, 0, -1])  # approach direction (down) 

                # PCA on surface points
                pca = PCA(n_components=3)
                pca.fit(surface_points)

                center = surface_points.mean(axis=0) # Center of the surface                

                # Opening direction = PCA component 1 (shorter in-plane axis)
                x_axis = pca.components_[1]
                x_axis = (x_axis - np.dot(x_axis, approach) * approach)  / np.linalg.norm(x_axis)
                y_axis = np.cross(approach, x_axis)
                R_ortho = np.stack([x_axis, y_axis, approach], axis=1)

                # added untwist: takes dot product between x-axis of frame and world x-axis. x-axis must always point in positive world x direction
                x_world = np.array([1, 0, 0])
                x_grasp = R_ortho[:, 0]  # X-axis of the grasp frame

                if np.dot(x_world, x_grasp) < 0: #dot=-1 oppisite direction, dot=1 same direction, dot=0 orthogonal
                    R_ortho[:, 0] *= -1  # Flip X
                    R_ortho[:, 1] *= -1  # Flip Y, Z stays the same

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

                if  grasp_width >= 0.15: # Grasp width too high
                    # Grasp width too big for grippers. Skip this one
                    continue

                if center[2] <= 0: # make sure z is above 0
                    continue

                grasps.append([float(center[0]), float(center[1]), float(center[2]), float(rpy[0]), float(rpy[1]), float(rpy[2]), float(grasp_width)])

                # Remove the group and stop
                del groups[idx]
                break

            if idx == len(groups) - 1: # if no top down grasp was found
                top_grasp = self.generate_top_down_grasp(pcd)
                grasps.append(top_grasp) 
                self.get_logger().info(f"Top-down grasp found using old top_grasp algorithm")
        

        if self.generate_general_grasp:
            if np.max(points[:, 2]) > 0.10: # if the object is close to table
                for group in groups:
                    if count >= num_candidates:
                        break

                    surface_points = points[group]
                    surface_normals = normals[group]

                    # Estimate approach vector (mean normal)
                    approach = -np.mean(surface_normals, axis=0)
                    approach /= np.linalg.norm(approach)

                    # PCA on surface points
                    pca = PCA(n_components=3)
                    pca.fit(surface_points)
                    
                    # shift grasp center to grasp higher on the object to avoid colliding with the table
                    if max(surface_points[:, 2]) - min(surface_points[:, 2]) > 0.03: # if the object is not flat eg. z variation > 3 cm
                        pc1 = pca.components_[0] # PCA component 1 (longer in-plane axis)
                        if np.dot(pc1,[0,0,1]) < 0: # If the PCA component is pointing downwards
                            pc1 = -pc1
                        grasp_height = 0.25 # Controls how far from top to grasp [%]
                        projections = surface_points @ pc1
                        proj_min = np.min(projections)
                        proj_max = np.max(projections)
                        target_proj = proj_max - grasp_height * (proj_max - proj_min)
                        mean_point = surface_points.mean(axis=0)
                        center = mean_point + pc1 * (target_proj - np.dot(mean_point, pc1))
                    else:
                        center = surface_points.mean(axis=0) # Center of the surface

                    # Opening direction = PCA component 1 (shorter in-plane axis)
                    x_axis = pca.components_[1]
                    y_axis = np.cross(approach, x_axis)

                    # Re-orthonormalize
                    R_matrix = np.stack([x_axis, y_axis, approach], axis=1)
                    U, _, Vt = np.linalg.svd(R_matrix)
                    R_ortho = U @ Vt

                    # added untwist: takes dot product between x-axis of frame and world x-axis. x-axis must always point in positive world y direction
                    x_world = np.array([1, 0, 0])
                    x_grasp = R_ortho[:, 0]  # X-axis of the grasp frame

                    if np.dot(x_world, x_grasp) < 0: #dot=-1 oppisite direction, dot=1 same direction, dot=0 orthogonal
                        R_ortho[:, 0] *= -1  # Flip X
                        R_ortho[:, 1] *= -1  # Flip Y, Z stays the same

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

                    # Collision check: does grasp collide with table?
                    grasp_half = (grasp_width / 2.0 + 0.05) # add 3 cm margin
                    pt_left = center - R_ortho[:, 0] * grasp_half
                    pt_right = center + R_ortho[:, 0] * grasp_half

                    if pt_left[2] < 0 or pt_right[2] < 0: # Must be above the table
                        # Grasp would penetrate the table → skip this one
                        self.get_logger().info(f"The found grasp would penetrate the table: {pt_left[2]}, {pt_right[2]}, trying to find grasp again")
                        continue

                    if  grasp_width >= 0.15: # Grasp width too high
                        # Grasp width too big for grippers. Skip this one
                        continue

                    # Add grasp to list [x, y, z, roll, pitch, yaw]
                    grasps.append([float(center[0]), float(center[1]), float(center[2]), float(rpy[0]), float(rpy[1]), float(rpy[2]), float(grasp_width)])
                    count += 1


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

    def project(self, pt3d):
        fx = self.camera_info[0]
        fy = self.camera_info[4]
        cx = self.camera_info[2]
        cy = self.camera_info[5]
        x, y, z = pt3d
        u = int((x * fx / z) + cx)
        v = int((y * fy / z) + cy)
        return (u, v)
    

    def generate_top_down_grasp(self,global_pointcloud, top_band_height=0.003):
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
        original_points = np.asarray(global_pointcloud)

        if pc.shape[0] == 0:
            print("No valid points in point cloud.")
            return []

        # Sort by Z (height)
        pc_sorted = pc[np.argsort(pc[:, 2])] 

        # Get the highest z value
        z_max = pc_sorted[-1, 2]

        if z_max < top_band_height:
            top_band_height = z_max

        # Select points within top_band_height of max height
        top_points = pc_sorted[pc_sorted[:, 2] >= (z_max - top_band_height)]

        while top_points.shape[0] < 3: # not enough points for PCA
            # Select points within top_band_height of max height
            top_band_height += 0.001
            top_points = pc_sorted[pc_sorted[:, 2] >= (z_max - top_band_height)]

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
        x_axis = (x_axis - np.dot(x_axis, approach) * approach)  / np.linalg.norm(x_axis)
        y_axis = np.cross(approach, x_axis)

        # Re-orthonormalize (ensures that no numerical errors occur in the calculated rotation matrix and that they are orthognormal) 
        R_ortho = np.stack([x_axis, y_axis, approach], axis=1)

        # added untwist: takes dot product between x-axis of frame and world x-axis. x-axis must always point in positive world y direction
        x_world = np.array([1, 0, 0])
        x_grasp = R_ortho[:, 0]  # X-axis of the grasp frame

        if np.dot(x_world, x_grasp) < 0: #dot=-1 oppisite direction, dot=1 same direction, dot=0 orthogonal
            R_ortho[:, 0] *= -1  # Flip X
            R_ortho[:, 1] *= -1  # Flip Y, Z stays the same

        # Convert to roll-pitch-yaw
        rpy = ROT.from_matrix(R_ortho).as_euler('xyz', degrees=True)

        #  Filter points near the x-Z plane (with threshold)
        z_threshold = 0.02  # 2 cm
        top_mask = (original_points[:, 2] > (z_max - z_threshold))
        plane_points = original_points[top_mask]

        if len(plane_points) < 2:
            grasp_width = 0.15  # Not enough data so max width
        else:
            # Project points onto x-axis to get scalar positions along grasp width direction
            projections = (plane_points - center) @ x_axis
            min_proj = np.min(projections)
            max_proj = np.max(projections)
            grasp_width = np.abs(max_proj - min_proj)

        if grasp_width < 0.01: # Grasp width too small 
            grasp_width = 0.01

        if center[2] <= 0: # Due to point_cloud errors, (unprecesion of +- 2cm of cam, or from callibration). this is added.
            center[2] = 0.002

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
        

    def get_color_image(self):
        return np.asanyarray(self.color_frame)

   
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
            self.get_logger().info(f"Converting depth to meters")
            z = self.depth_frame[pixel_y, pixel_x] / 1000 # Convert to meters

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

def main(args=None):
    rclpy.init(args=args)

    # Create an ObjectDetector instance
    detector = ObjectDetector()

    #this was commented out
    rclpy.spin(detector) 

    rclpy.shutdown()

if __name__ == '__main__':
    main()