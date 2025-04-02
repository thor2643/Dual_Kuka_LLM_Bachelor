import numpy as np
import cv2
import glob
from cv_bridge import CvBridge, CvBridgeError

#ROS stuff
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import DefineObjectInfo
from geometry_msgs.msg import Point
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import os
import tf2_ros
from geometry_msgs.msg import TransformStamped
import math

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
        self.K_cam = [  [909.85, 0, 646.6],
                        [0, 909.57, 386.43],
                        [0, 0, 1]]  # Camera matrix

        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        self.image_dir = "calibration_images"
        os.makedirs(self.image_dir, exist_ok=True)

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

    def capture_data(self):
        self.retrieve_aligned_frames()

        image = self.get_color_image()
        point_cloud = self.get_depth_image()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

        image_w_markers = cv2.aruco.drawDetectedMarkers(image, corners, ids)

        while True:
            cv2.imshow("ArUCo Tag", image_w_markers)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        # Estimate Aruco pose
        markerLength = 68 #mm
        camMatrix = np.array(self.camera.camera_info_k).reshape(3, 3)
        distCoeffs = np.array(self.camera.camera_info_d)

        objPoints = np.zeros((4, 1, 3), np.float32)
        objPoints[0] = np.array([-markerLength/2, markerLength/2, 0])
        objPoints[1] = np.array([markerLength/2, markerLength/2, 0])
        objPoints[2] = np.array([markerLength/2, -markerLength/2, 0])
        objPoints[3] = np.array([-markerLength/2, -markerLength/2, 0])
 
        nMarkers = len(corners)
        rvecs = np.zeros((nMarkers, 3))
        tvecs = np.zeros((nMarkers, 3))

        if nMarkers > 0:
            for i in range(nMarkers):
                _, rvec, tvec = cv2.solvePnP(objPoints, corners[i], camMatrix, distCoeffs)
                rvecs[i] = rvec.flatten()
                tvecs[i] = tvec.flatten()
                image = cv2.drawFrameAxes(image, camMatrix, distCoeffs, rvecs[i], tvecs[i], markerLength)

        while True:
            cv2.imshow("ArUCo Tag", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        # Save the image with markers
        save_dir = os.path.join(self.image_dir, f"{self.capture_id}")
        os.makedirs(save_dir, exist_ok=True)

        img_filename = os.path.join(save_dir, "image_with_markers.png")
        cv2.imwrite(img_filename, image)

        # Save rvecs and tvecs
        rvecs_filename = os.path.join(save_dir, "rvecs.npy")
        tvecs_filename = os.path.join(save_dir, "tvecs.npy")
        np.save(rvecs_filename, rvecs)
        np.save(tvecs_filename, tvecs)

        self.get_logger().info(f"Saved image with markers to {img_filename}")
        self.get_logger().info(f"Saved rvecs to {rvecs_filename}")
        self.get_logger().info(f"Saved tvecs to {tvecs_filename}")

        self.capture_id += 1
        
        rclpy.spin_once(self, timeout_sec=0.1)

        # Get gripper pose
        try:
            transform_3: TransformStamped = self.tf_buffer.lookup_transform(
                "world", "2f_tool0", rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=2.0))

            # Assuming transform_3 is your TransformStamped object
            quaternion = [
                transform_3.transform.rotation.w,
                transform_3.transform.rotation.x,
                transform_3.transform.rotation.y,
                transform_3.transform.rotation.z,
            ]

            # Convert quaternion to Euler angles
            roll, pitch, yaw = self.quaternion_to_euler_angle(*quaternion)
            print(f"Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}")

            R = np.array([roll, pitch, yaw])
            t = np.array([
                [transform_3.transform.translation.x],
                [transform_3.transform.translation.y],
                [transform_3.transform.translation.z]
            ])

            #self.get_logger().info(f"Captured data point {len(self.imgpoints)}")

            # Print the transform
            #self.get_logger().info(f"Gripper pose R: {R}")
            #self.get_logger().info(f"Gripper pose t: {t}")

            # Save the transform to the save_dir directory
            transform_filename = os.path.join(save_dir, "gripper_pose.npz")
            np.savez(transform_filename, R=R, t=t)
            self.get_logger().info(f"Saved gripper pose to {transform_filename}")
            return True
        except tf2_ros.LookupException:
            self.get_logger().error("Failed to get gripper pose")
            return False
        
        
        

    def calibrate(self):
        if len(self.objpoints) < 10:
            self.get_logger().error("Not enough data points for calibration")
            return

        R_gripper2base = [pose[0] for pose in self.gripper_poses]
        t_gripper2base = [pose[1] for pose in self.gripper_poses]
        R_target2cam = [pose[0] for pose in self.gripper_poses]
        t_target2cam = [pose[1] for pose in self.gripper_poses]

        """
        ret, R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(
            R_gripper2base, t_gripper2base, R_target2cam, t_target2cam)

        if ret:
            self.get_logger().info("Hand-eye calibration successful")
            self.get_logger().info(f"R_cam2gripper: {R_cam2gripper}")
            self.get_logger().info(f"t_cam2gripper: {t_cam2gripper}")
        else:
            self.get_logger().error("Hand-eye calibration failed")"
        """

    def estimate_camera_pose(self):
        if len(self.objpoints) == 0 or len(self.imgpoints) == 0:
            self.get_logger().error("No data points available for pose estimation")
            return None, None

        # Camera matrix and distortion coefficients
        if self.camera.camera_info_k is None or self.camera.camera_info_d is None:
            self.get_logger().error("Camera info not available")
            return None, None

        #TODO: Get camera matrix and distortion coefficients from camera_info
        camera_matrix = np.array(self.camera.camera_info.k).reshape(3, 3)
        dist_coeffs = np.array(self.camera.camera_info.d)

        # Solve PnP to estimate pose
        ret, rvec, tvec = cv2.solvePnP(
            self.objpoints[-1],  # Last set of 3D points
            self.imgpoints[-1],  # Last set of 2D points
            camera_matrix,
            dist_coeffs
        )

        if ret:
            R_cam2target, _ = cv2.Rodrigues(rvec)
            t_cam2target = tvec
            self.get_logger().info(f"Estimated R_cam2target: {R_cam2target}")
            self.get_logger().info(f"Estimated t_cam2target: {t_cam2target}")
            return R_cam2target, t_cam2target
        else:
            self.get_logger().error("Pose estimation failed")
            return None, None

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

    def run(self):
        self.get_logger().info("Press 'c' to capture data, 'q' to quit and calibrate and 'm' to generate ArUco marker")
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            key = input("Input: ")
            if key == 'c':
                self.capture_data()
            elif key == 'm':
                self.generate_aruco_marker()
            elif key == 'q':
                self.calibrate()
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