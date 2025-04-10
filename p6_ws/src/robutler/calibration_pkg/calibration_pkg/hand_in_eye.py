import numpy as np
import cv2
import glob
from cv_bridge import CvBridge, CvBridgeError

#ROS stuff
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import os
import tf2_ros
from geometry_msgs.msg import TransformStamped
import math
import json
from scipy.spatial.transform import Rotation   

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
        self.camera_info_k = None
        self.camera_info_d = None

        
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
        self.camera_info_k = msg.k
        self.camera_info_d = msg.d
 

#cv2.calibrateHandEye()
class HandEyeCalibrationNode(Node):
    def __init__(self):
        super().__init__('hand_eye_calibration_node')

        self.get_logger().info("Initializing HandEyeCalibrationNode")

        self.camera = RealSenseCamera()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.objpoints = []  # 3D points in real world space
        self.imgpoints = []  # 2D points in image plane
        self.gripper_poses = []  # Gripper poses
        self.K_cam = [[900.66004528,   0.,         636.58619713],
                        [  0.,         899.46047703, 358.64746603],
                        [  0.,           0.,           1.,        ]]  # Camera matrix
        
        self.D_cam = [[ 0.0949935, -0.05628258, -0.00132729, -0.0034892, -0.40672554]]  # Distortion coefficients

        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        self.handeye_data_dir = "handeye_calibration_data"
        self.camera_data_dir = "camera_calibration_images"
        os.makedirs(self.handeye_data_dir, exist_ok=True)
        os.makedirs(self.camera_data_dir, exist_ok=True)

        self.depth_frame = None
        self.color_frame = None
        self.camera_info_k = None
        self.camera_info_d = None

        self.capture_id = 0

        self.get_logger().info("HandEyeCalibrationNode initialized")

    def retrieve_aligned_frames(self):      
        # Retrieve aligned frames from the RealSense camera by spinning the node untill new frames are available

        while self.camera.depth_img is None or self.camera.color_img is None or self.camera.camera_info_k is None or self.camera.camera_info_d is None:
                rclpy.spin_once(self.camera)

        while np.array_equal(self.camera.depth_img, self.depth_frame) or np.array_equal(self.camera.color_img, self.color_frame):
                rclpy.spin_once(self.camera)
        
        self.depth_frame = self.camera.depth_img
        self.color_frame = self.camera.color_img
        self.camera_info_k = self.camera.camera_info_k
        self.camera_info_d = self.camera.camera_info_d

    def get_color_image(self):
        return np.asanyarray(self.color_frame)
    
    def get_depth_image(self):
        # Convert the depth frame to a NumPy array
        return np.asanyarray(self.depth_frame)
    
    def get_cartesian_coordinates(self, pixel_x, pixel_y):
        # The camera info message .K contains the camera intrinsics
        #[ fx   0  cx ]
        #[  0  fy  cy ]
        #[  0   0   1 ]

        camMatrix = np.array(self.camera.camera_info_k)

        # Get the camera intrinsics
        fx = camMatrix[0]
        fy = camMatrix[4]
        cx = camMatrix[2]
        cy = camMatrix[5]

        if pixel_x < 0 or pixel_x >= self.depth_frame.shape[1] or pixel_y < 0 or pixel_y >= self.depth_frame.shape[0]:
            print("Pixel coordinates out of bounds.")
            return None
        
        if self.depth_frame[pixel_y, pixel_x] == 0:
            print("No depth data available at the selected pixel.")
            return None

        # Calculate the x, y, z coordinates
        z = self.depth_frame[pixel_y, pixel_x] / 1000  # Convert to meters
        x = ((pixel_x - cx) * z / fx) 
        y = ((pixel_y - cy) * z / fy) 

        return np.array([x, y, z])
    
    def kabsch_algorithm(self, P_camera, P_world):
        # Compute centroids 
        C_camera = np.mean(P_camera, axis=0) 
        C_world = np.mean(P_world, axis=0) 
        
        # Center the points 
        P_camera_centered = P_camera - C_camera 
        P_world_centered = P_world - C_world 
        
        # Compute covariance matrix 
        H = np.dot(P_camera_centered.T, P_world_centered) 
        
        # Singular Value Decomposition 
        U, S, Vt = np.linalg.svd(H) 
        
        # Compute rotation 
        R = np.dot(Vt.T, U.T) 
        
        # Ensure a proper rotation matrix (det(R) should be +1) 
        if np.linalg.det(R) < 0: 
            Vt[2, :] *= -1 
            R = np.dot(Vt.T, U.T) 
        
        # Compute translation 
        t = C_world - np.dot(R, C_camera) 
        
        
        # Construct transformation matrix 
        T = np.eye(4) 
        T[:3, :3] = R 
        T[:3, 3] = t 

        print("Transformation matrix:")
        print(T)

        return R, t

    def capture_data(self, use_color=True, use_depth=False):
        # General checks
        if not use_color and not use_depth:
            self.get_logger().error("Please select at least one of the two options: use_color or use_depth")
            return False
        
        self.retrieve_aligned_frames()

        image = self.get_color_image()
        original_image = image.copy()
        image_depth = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #TODO: add easy variable definition
        # Define variables (customise for your case)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
        markerLength = 0.025        # in meters
        markerSeparation = 0.0085   # in meters (adjust based on your board layout)
        board_size = (6, 8)         # columns x rows (adjust as per your board)
        world_link = "world"        # The world frame name
        gripper_link = "2f_tool0"   # The gripper frame name


        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

        image_w_markers = cv2.aruco.drawDetectedMarkers(image, corners, ids)

        while True:
            cv2.imshow("ArUCo Tag", image_w_markers)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
                
        poses = {}
        poses['board'] = {}

        if use_color:

            # ------------------- Estimate the pose of the board ------------------- #

            # Define the board layout
            board = cv2.aruco.GridBoard(
                size=(board_size[0], board_size[1]),  # columns x rows (adjust as per your board)
                markerLength=markerLength,
                markerSeparation=markerSeparation,
                dictionary=aruco_dict
            )

            # Contains calibrated values for the RGB camera
            camMatrix = np.array(self.K_cam)
            distCoeffs = np.array(self.D_cam)

            # Find corresponding 3D points in the world and 2D points in the image
            objPoints, imagePoints = board.matchImagePoints(corners, ids)

            # Solve PnP to get the rotation and translation vectors
            _, rvec, tvec = cv2.solvePnP(objPoints, imagePoints, camMatrix, distCoeffs)

            image = cv2.drawFrameAxes(image, camMatrix, distCoeffs, rvec, tvec, markerLength)

            # Convert rotation vector to Euler angles
            R_board2cam, _ = cv2.Rodrigues(rvec)
            r = Rotation.from_matrix(R_board2cam)
            angles = r.as_euler("xyz", degrees=True)

            board_pose = {
                "r_vec": angles.flatten().tolist(),
                "t_vec": tvec.flatten().tolist()
            }

            poses['board'] = board_pose

            # ------------------- Estimate the pose of each marker ------------------- #

            # Draw the individual axes on the image
            objPoints = np.zeros((4, 1, 3), np.float32)
            objPoints[0] = np.array([-markerLength/2, markerLength/2, 0])
            objPoints[1] = np.array([markerLength/2, markerLength/2, 0])
            objPoints[2] = np.array([markerLength/2, -markerLength/2, 0])
            objPoints[3] = np.array([-markerLength/2, -markerLength/2, 0])

            nMarkers = len(corners)

            if nMarkers > 0:
                for i in range(nMarkers):
                    poses[int(ids[i][0])] = {}

                    _, rvec, tvec = cv2.solvePnP(objPoints, corners[i], camMatrix, distCoeffs)

                    # Convert Rodrigues vector to rotation matrix
                    R_target2cam, _ = cv2.Rodrigues(rvec)

                    ### first transform the matrix to euler angles
                    r =  Rotation.from_matrix(R_target2cam)
                    angles = r.as_euler("xyz",degrees=True)

                    poses[int(ids[i][0])] = {"r_vec": angles.flatten().tolist(), "t_vec": tvec.flatten().tolist()}

                    image = cv2.drawFrameAxes(image, camMatrix, distCoeffs, rvec, tvec, markerLength)   

        if use_depth:

            # ------------------- Estimate the pose of the board using depth and Kabsch ------------------- #

            poses['board_depth'] = {}

            # Used to draw frames
            camMatrix = np.array(self.camera.camera_info_k).reshape(3, 3)
            distCoeffs = np.array(self.camera.camera_info_d)

            board = cv2.aruco.GridBoard(
                size=(board_size[0], board_size[1]),
                markerLength=markerLength,
                markerSeparation=markerSeparation,
                dictionary=aruco_dict
            )

            # Find corresponding 3D points in the world and 2D points in the image
            objPoints, imagePoints = board.matchImagePoints(corners, ids)

            P_camera = []
            P_world = []

            for obj_pt, img_pt in zip(objPoints, imagePoints):
                u, v = int(img_pt[0][0]), int(img_pt[0][1])

                cam_3d = self.get_cartesian_coordinates(u, v)
                P_camera.append(cam_3d)
                P_world.append(obj_pt[0])

            if len(P_camera) >= 3:
                P_camera = np.array(P_camera)
                P_world = np.array(P_world)

                R, t = self.kabsch_algorithm(P_world, P_camera)

                # Convert rotation matrix to Euler angles
                r = Rotation.from_matrix(R)
                angles = r.as_euler("xyz", degrees=True)

                poses['board_depth'] = {
                    "r_vec": angles.flatten().tolist(),
                    "t_vec": t.flatten().tolist()
                }

                # Optional: draw axes for visualization
                rvec, _ = cv2.Rodrigues(R)
                image_depth = cv2.drawFrameAxes(image_depth, camMatrix, distCoeffs, rvec, t, markerLength)

        while True:
            cv2.imshow("ArUCo Board Pose", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


        # Save the image with markers
        save_dir = os.path.join(self.handeye_data_dir, f"{self.capture_id}")
        os.makedirs(save_dir, exist_ok=True)

        img_filename = os.path.join(save_dir, "image_with_markers.png")
        img_filename_original = os.path.join(save_dir, "image.png")
        img_filename_depth = os.path.join(save_dir, "image_depth.png")
        cv2.imwrite(img_filename, image)
        cv2.imwrite(img_filename_original, original_image)
        cv2.imwrite(img_filename_depth, image_depth)

        # Save poses dictionary
        poses_filename = os.path.join(save_dir, "poses.json")
        with open(poses_filename, 'w') as f:
            json.dump(poses, f, indent=4)

        self.get_logger().info(f"Saved image with markers to {img_filename}")
        self.get_logger().info(f"Saved rvecs and tvecs to {poses_filename}")

        self.capture_id += 1
        
        rclpy.spin_once(self, timeout_sec=0.1)

        # Get gripper pose (try a few times if not successful)
        for i in range(5):
            try:
                transform_3: TransformStamped = self.tf_buffer.lookup_transform(
                    world_link, gripper_link, rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=2.0))

                # Assuming transform_3 is your TransformStamped object
                quaternion = [
                    transform_3.transform.rotation.w,
                    transform_3.transform.rotation.x,
                    transform_3.transform.rotation.y,
                    transform_3.transform.rotation.z,
                ]

                # Convert quaternion to Euler angles
                roll, pitch, yaw = self.quaternion_to_euler_angle(*quaternion)
                
                # This is not actual roll, pitch, yaw. It is the Rodrigues vector
                R = {"roll": roll, "pitch": pitch, "yaw": yaw}
                t = {
                    "x": transform_3.transform.translation.x,
                    "y": transform_3.transform.translation.y,
                    "z": transform_3.transform.translation.z
                }

                # Save the transform as a JSON dictionary
                transform_data = {
                    "R": R,
                    "t": t
                }

                transform_filename = os.path.join(save_dir, "gripper_pose.json")
                with open(transform_filename, 'w') as f:
                    json.dump(transform_data, f, indent=4)
                self.get_logger().info(f"Saved gripper pose to {transform_filename}")
                return True
            except tf2_ros.LookupException:
                if i < 4:
                    self.get_logger().info("Retrying...")
                    rclpy.spin_once(self, timeout_sec=0.1)
                else:
                    self.get_logger().error("Failed to get gripper pose after multiple attempts")
                    return False
        
    def capture_images(self):
        self.retrieve_aligned_frames()

        image = self.get_color_image()

        # Save the images
        save_dir = self.camera_data_dir
        os.makedirs(save_dir, exist_ok=True)

        img_filename = os.path.join(save_dir, f"image{self.capture_id}.png")

        cv2.imwrite(img_filename, image)

        self.get_logger().info(f"Saved image to {img_filename}")

        self.capture_id += 1
        
    def load_poses_from_folder(self, folder_path, id="1"):
        gripper_poses = []
        target_to_cam_poses = []

        for subfolder in sorted(os.listdir(folder_path), key=lambda x: int(x)):
            subfolder_path = os.path.join(folder_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue

            gripper_pose_path = os.path.join(subfolder_path, "gripper_pose.json")
            poses_path = os.path.join(subfolder_path, "poses.json")

            if not os.path.exists(gripper_pose_path) or not os.path.exists(poses_path):
                continue

            with open(gripper_pose_path, "r") as f:
                gripper_data = json.load(f)
                roll, pitch, yaw = gripper_data["R"]["roll"], gripper_data["R"]["pitch"], gripper_data["R"]["yaw"]
                #R_gripper = cv2.Rodrigues(np.array([roll, pitch, yaw]))[0]
                R_gripper = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=True).as_matrix()
                t_gripper = np.array([gripper_data["t"]["x"], gripper_data["t"]["y"], gripper_data["t"]["z"]])

                gripper_poses.append((R_gripper, t_gripper))

            with open(poses_path, "r") as f:
                target_data = json.load(f)
                for marker_id, pose in target_data.items():
                    if marker_id == id:
                        r_vec = np.array(pose["r_vec"])
                        t_vec = np.array(pose["t_vec"])
                        #R_target = cv2.Rodrigues(r_vec)[0]
                        R_target = Rotation.from_euler("xyz", r_vec, degrees=True).as_matrix()
                        target_to_cam_poses.append((R_target, t_vec))
                        #target_to_cam_poses.append((r_vec, t_vec))
                        break
                    else:
                        continue

        return gripper_poses, target_to_cam_poses 
        

    def calibrate(self, depth_data_available=True, color_data_available=True):
        # https://users.cs.utah.edu/~srikumar/cv_spring2017_files/Lecture3.pdf
        self.get_logger().info("Starting calibration")

        if not os.path.exists(self.handeye_data_dir):
            self.get_logger().error("No calibration folder data found")
            return
        if not depth_data_available and not color_data_available:
            self.get_logger().error("Neither depth nor color data is available for calibration")
            return
        
        callibration_methods = [cv2.CALIB_HAND_EYE_TSAI,  
                                cv2.CALIB_HAND_EYE_PARK,
                                cv2.CALIB_HAND_EYE_HORAUD, 
                                cv2.CALIB_HAND_EYE_ANDREFF,
                                cv2.CALIB_HAND_EYE_DANIILIDIS,]
        
        method_names = ["TSAI", "ANDREFF", "DANIILIDIS", "HORAUD", "PARK"]
        
        # Loop through each calibration method
        for method in callibration_methods:
            self.get_logger().info(f"Using method: {method}")

            for i in range(2):
                if depth_data_available and i == 0:
                    # Load poses
                    gripper_poses, target_to_cam_poses = self.load_poses_from_folder(self.handeye_data_dir, id="board_depth")
                    data_type = "depth"
                elif color_data_available and i == 1:
                    # Load poses
                    gripper_poses, target_to_cam_poses = self.load_poses_from_folder(self.handeye_data_dir, id="board")
                    data_type = "color"
                else:
                    continue

                if len(gripper_poses) < 4 or len(target_to_cam_poses) < 4:
                    self.get_logger().error("Not enough data points for calibration")
                    return

                R_gripper2base = [pose[0] for pose in gripper_poses]
                t_gripper2base = [pose[1] for pose in gripper_poses]
                R_target2cam = [pose[0] for pose in target_to_cam_poses]
                t_target2cam = [pose[1] for pose in target_to_cam_poses]

                # Perform hand-eye calibration
                R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(
                    R_gripper2base, t_gripper2base, R_target2cam, t_target2cam, method=method
                )

                if R_cam2gripper is not None and t_cam2gripper is not None:
                    self.get_logger().info(f"Hand-eye calibration from {data_type, method_names[method]} successful")
                    self.get_logger().info(f"""\n\nR_cam2gripper:\n {R_cam2gripper}\n
                                        \nt_cam2gripper:\n {t_cam2gripper}\n""")
                    
                    # Save the calibration results
                    save_dir = "CalibrationResults"
                    os.makedirs(save_dir, exist_ok=True)
                    calibration_filename = os.path.join(save_dir, "hand_eye_calibration.json")
                    
                    # Load existing data if the file exists
                    if os.path.exists(calibration_filename):
                        with open(calibration_filename, 'r') as f:
                            calibration_data = json.load(f)
                    else:
                        calibration_data = {}

                    # Update the calibration data
                    if method_names[method] not in calibration_data:
                        calibration_data[method_names[method]] = {}
                    
                    calibration_data[method_names[method]][data_type] = {
                        "R_cam2gripper": R_cam2gripper.tolist(),
                        "t_cam2gripper": t_cam2gripper.tolist()
                    }

                    # Save the updated calibration data
                    with open(calibration_filename, 'w') as f:
                        json.dump(calibration_data, f, indent=4)
                    self.get_logger().info(f"Saved calibration data to {calibration_filename}")

                else:
                    self.get_logger().error("Hand-eye calibration failed")

    def calibrate_camera(self):
        # Set your parameters here
        checkerboard_size = (17, 24)  # inner corners per row and column
        square_size = 7.5  # mm
        image_folder = self.camera_data_dir

        # Prepare object points (0,0,0), (1,0,0), ..., (16,23,0) multiplied by square size
        objp = np.zeros((checkerboard_size[1] * checkerboard_size[0], 3), np.float32)
        objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
        objp *= square_size

        # Arrays to store object points and image points
        objpoints = []  # 3d points in real world
        imgpoints = []  # 2d points in image plane

        # Load all image paths from the folder
        images = glob.glob(os.path.join(image_folder, '*.png'))  # or '*.png' etc.

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the checkerboard corners
            ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

            if ret:
                objpoints.append(objp)
                # Refine corner locations
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1),
                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                )
                imgpoints.append(corners2)

                # Optional: Draw and display the corners
                cv2.drawChessboardCorners(img, checkerboard_size, corners2, ret)
                cv2.imshow('Corners', img)
                cv2.waitKey(100)

        cv2.destroyAllWindows()

        # Calibration
        ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )

        # Print results
        print("Camera matrix:\n", camera_matrix)
        print("\nDistortion coefficients:\n", dist_coeffs)
        print("\nRe-projection error:", ret)
        
    def quaternion_to_euler_angle(self, w, x, y, z):
        ysqr = y * y

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + ysqr)
        X = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        Z = math.degrees(math.atan2(t3, t4))

        return X, Y, Z

    def generate_aruco_marker(self):
        print("Generating ArUco marker")

        spacing = 25
        size = 200
        shape = (3, 2)
        marker_image = np.ones((shape[0]*(size+spacing)+spacing, shape[1]*(size+spacing)+spacing, 1), dtype=np.uint8) * 255

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

        for i in range(shape[0]):
            for j in range(shape[1]):
                #img = np.zeros((size, size), dtype=np.uint8)
                img = cv2.aruco.generateImageMarker(aruco_dict, (i*shape[1])+j+1, size)
                marker_image[spacing+i*(size+spacing):(i+1)*(size+spacing), spacing + j*(size+spacing):(j+1)*(size+spacing), 0] = img
                

        cv2.imwrite("aruco_marker.png", marker_image)
        self.get_logger().info("ArUco marker generated and saved at aruco_marker.png")

        while True:
            cv2.imshow("ArUCo Tag", marker_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def generate_aruco_board(self):
        print("Generating ArUco board")
        markerLength = 0.03 #m
        markerSeparation = 0.01 #m
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

        board = cv2.aruco.GridBoard(
            size=(6, 8),
            markerLength=markerLength,
            markerSeparation=markerSeparation,
            dictionary=aruco_dict
        )

        board_image = board.generateImage((600, 800))

        cv2.imwrite("aruco_board.png", board_image)
        self.get_logger().info("ArUco board generated and saved at aruco_board.png")
        while True:
            cv2.imshow("ArUCo Board", board_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


    def run(self):
        self.get_logger().info("\n\nPress:\n 'c' to capture data\n 'k' to capture and save images\n 'g' for calibrate camera\n 'h' to make hand-eye-calibration\n 'm' to generate ArUco marker\n 'b' to create aruco board\n 'q' to quit")
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            key = input("Input: ")
            if key == 'c':
                self.capture_data(use_depth=True, use_color=True)
            elif key == 'k':
                self.capture_images()
            elif key == 'g':
                self.calibrate_camera()
            elif key == 'h':
                self.calibrate()
            elif key == 'm':
                self.generate_aruco_marker()
            elif key == 'b':
                self.generate_aruco_board()
            elif key == 'q':
                break


def main(args=None):
    rclpy.init(args=args)
    node = HandEyeCalibrationNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()