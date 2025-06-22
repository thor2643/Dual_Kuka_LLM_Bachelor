# Import libraries
import json
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import numpy as np
from threading import Event
import base64
import cv2
from cv_bridge import CvBridge, CvBridgeError
from scipy.spatial.transform import Rotation 
import math
import time
from utils.mode_switch import load_use_sim, set_use_sim
from utils.linear_alg_utils import (
    build_transform_matrix_from_rpy, 
    get_zyz_transform, 
    invert_transformation_matrix, 
    euler_to_quat,
    quat_to_euler,
    T_mat_from_Rotm_tvec,
    flip_if_near_180
)

from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


# ROS 2 libraries and Node structure
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import tf2_ros

# ROS 2 messages
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import PlanMoveCommand
from project_interfaces.srv import ExecuteMoveCommand
from project_interfaces.srv import PromptJanice
from project_interfaces.srv import GetCurrentPose
from project_interfaces.srv import GripperMoveit
from project_interfaces.srv import GetObjectInfo, PlanMoveCommand, ExecuteMoveCommand, PromptJanice, GetCurrentPose
from project_interfaces.msg import TransformMatrix, Grasp6D, DetectedObject
from robotiq_3f_gripper_ros2_interfaces.srv import Robotiq3FGripperOutputService
from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperInputRegisters
from robotiq_2f_85_interfaces.srv import Robotiq2F85GripperCommand
from project_interfaces.srv import GetImage
from project_interfaces.srv import GetSimCameraData
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Image, JointState

class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client')

        client_cb_group = MutuallyExclusiveCallbackGroup()
        gui_service_cb_group = MutuallyExclusiveCallbackGroup()

        self.srv = self.create_service(
            PromptJanice, 'send_prompt', self.main_handle_service, callback_group=gui_service_cb_group
        )
        self.get_logger().info('Service Server is ready.')

        # Gripper service client
        self._3f_controller = Robotiq3FGripperOutputService.Request()
        self._3f_controller_cli = self.create_client(Robotiq3FGripperOutputService, "Robotiq3FGripper/OutputRegistersService", callback_group=client_cb_group)

        self._2f_client = self.create_client(Robotiq2F85GripperCommand, 'gripper_2f_service', callback_group=client_cb_group)
        self._2f_req = Robotiq2F85GripperCommand.Request()
        
        self._3f_input_registers = Robotiq3FGripperInputRegisters()
        self._3f_input_subscription = self.create_subscription(Robotiq3FGripperInputRegisters, "Robotiq3FGripper/InputRegisters", self.update_register, 10)

        # Moveit gripper clientNone
        self._gripper_client = self.create_client(GripperMoveit, 'gripper_moveit', callback_group=client_cb_group) 
        self._gripper_req = GripperMoveit.Request()

        #Object detector service client
        self.detector_client = self.create_client(GetObjectInfo, 'get_object_info', callback_group=client_cb_group)
        self.detector_req = GetObjectInfo.Request()
        self.objects_on_table = {}

        self.get_image_client = self.create_client(GetImage, 'get_image_from_rviz')
        self.get_image_req = GetImage.Request()

        # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/color/image_raw',  # Topic name
            self.convert_to_color_img,  # Callback function
            10  # Queue size
        )

        # Create a service client for the simulated camera data
        self.sim_cam_client = self.create_client(GetSimCameraData, 'get_simulated_camera_data', callback_group=client_cb_group)
        self.sim_cam_req = GetSimCameraData.Request()

        self.bridge = CvBridge()
        self.color_img = None
        self.use_sim = load_use_sim()

        # Robot service client
        self.robot_plan_client = self.create_client(PlanMoveCommand, 'plan_move_command', callback_group=client_cb_group)
        self.robot_plan_req = PlanMoveCommand.Request()

        self.robot_execute_client = self.create_client(ExecuteMoveCommand, 'execute_move_command', callback_group=client_cb_group)
        self.robot_execute_req = ExecuteMoveCommand.Request()

        self.robot_pose_client = self.create_client(GetCurrentPose, 'get_pose', callback_group=client_cb_group)
        self.robot_pose_req = GetCurrentPose.Request()

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Subscriber to the robot's joint values (Needed for grasp success check)
        self._3f_joint_values_mock = [0.0] * 11
        self._2f_joint_values_mock = [0.0] * 3
        self.joint_values_subscription = self.create_subscription(JointState, 'joint_states', self.joint_values_callback, 1)

        # Get current time and date from OS and format it for log file differentiation
        self.current_time = os.popen('date +"%Y-%m-%d_%H-%M-%S"').read().strip()
        self.get_logger().info(f"Current time and date: {self.current_time}")
        
        self.object_file = 'src/robutler/object_detector/object_detector/lego_bricks_config.json'
        self.conversation_log_folder = 'src/robutler/janise/resource/conversation_logs'
        self.conversation_log_file = self.conversation_log_folder + f'/{self.current_time}.json'

        # Create the directory if it doesn't exist
        if not os.path.exists(self.conversation_log_folder):
            os.makedirs(self.conversation_log_folder)

        # Define the locations in the environment
        self.coordinates = { # Predefined poses for different locations
            'HOME_RIGHT_ARM': {'x': '0', 'y': '0.15', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'},
            'HOME_LEFT_ARM': {'x': '1', 'y': '0.15', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'},
        } 
        
        #'ORGANIC_DROP': {'x': '0.49', 'y': '0.25', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '90'},
        #'RECYCLE_DROP': {'x': '0.38', 'y': '0.25', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '90'},
        #'WASTE_DROP': {'x': '0.60', 'y': '0.25', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '90'},
        #'TAKE_IMAGE': {'x': '0.42', 'y': '0.83', 'z': '0.5', 'roll': '-3', 'pitch': '-43', 'yaw': '-83'},

         # Cell state
        self.right_gripper_state = "Open"
        self.left_gripper_state = "Open"

        # Finale tool list
        self.sim_tool_list = {}
        self.tool_calls_path = 'src/robutler/janise/resource/tool_calls.json'

        self.user_prompt = None

    #######################################################################################
    # --------------------------------- EXTRA FUNCTIONS --------------------------------- #
    #######################################################################################

    def joint_values_callback(self, msg):
        # Reset joint arrays
        self._3f_joint_values_mock = [0.0] * 11
        self._2f_joint_values_mock = [0.0] * 3

        for i, joint_name in enumerate(msg.name):
            # 2F gripper joints
            if joint_name == "left_2f_robotiq_85_left_knuckle_joint":
                self._2f_joint_values_mock[0] = msg.position[i]
            elif joint_name == "left_2f_robotiq_85_left_finger_tip_joint":
                self._2f_joint_values_mock[1] = msg.position[i]
            elif joint_name == "left_2f_robotiq_85_left_finger_joint":
                self._2f_joint_values_mock[2] = msg.position[i]

            # 3F gripper joints
            elif joint_name == "a_3f_palm_finger_1_joint":
                self._3f_joint_values_mock[0] = msg.position[i]
            elif joint_name == "a_3f_finger_middle_joint_3":
                self._3f_joint_values_mock[1] = msg.position[i]
            elif joint_name == "a_3f_finger_2_joint_3":
                self._3f_joint_values_mock[2] = msg.position[i]
            elif joint_name == "a_3f_finger_2_joint_1":
                self._3f_joint_values_mock[3] = msg.position[i]
            elif joint_name == "a_3f_finger_middle_joint_1":
                self._3f_joint_values_mock[4] = msg.position[i]
            elif joint_name == "a_3f_finger_2_joint_2":
                self._3f_joint_values_mock[5] = msg.position[i]
            elif joint_name == "a_3f_palm_finger_2_joint":
                self._3f_joint_values_mock[6] = msg.position[i]
            elif joint_name == "a_3f_finger_1_joint_3":
                self._3f_joint_values_mock[7] = msg.position[i]
            elif joint_name == "a_3f_finger_1_joint_1":
                self._3f_joint_values_mock[8] = msg.position[i]
            elif joint_name == "a_3f_finger_middle_joint_2":
                self._3f_joint_values_mock[9] = msg.position[i]
            elif joint_name == "a_3f_finger_1_joint_2":
                self._3f_joint_values_mock[10] = msg.position[i]
    
    def get_image(self):
        # Returns the resized image from the camera, either from simulation or the real one.

        if load_use_sim():
            original_image = cv2.imread("resized_image.jpg")
            
            for i in range(4):
                request = GetSimCameraData.Request()
                future = self.sim_cam_client.call_async(request)

                # Wait for the result
                response = self.wait_future(future, timeout=15)

                if response is not None:
                    response = future.result()

                    color_img_rgb = self.bridge.imgmsg_to_cv2(response.color_image, desired_encoding="rgb8")
                    self.color_img_sim = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)
                    original_image = self.color_img_sim

                    break
                else:
                    if i == 4:
                        self.get_logger().error("Failed to retrieve image from simulated camera after multiple attempts")
                        original_image = cv2.imread("resized_image.jpg")
                    else:
                        self.get_logger().info("Retrying to get simulated camera data...")
                        rclpy.spin_once(self, timeout_sec=0.1)
                        continue
        
        else:
            original_image = self.color_img

        resized_image = cv2.resize(original_image, (524, 524))
        resized_image_path = "resized_image.jpg"
        cv2.imwrite(resized_image_path, resized_image)

        # Encode the resized image
        image = self.encode_image(resized_image_path)

        return image
        

    def convert_to_color_img(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            color_img_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR by default)
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting color image: {e}')
            
    def update_register(self, msg):
        self._3f_input_registers.g_sta = msg.g_sta
    	

    # Implemented to handle nested callbacks
    # Principle taken from https://gist.github.com/driftregion/14f6da05a71a57ef0804b68e17b06de5
    def wait_future(self, future, timeout=10):
        event=Event()

        def done_callback(future):
            nonlocal event
            event.set()

        future.add_done_callback(done_callback)

        # Wait for action to be done
        # self.service_done_event.wait()
        event_occured = event.wait(timeout)

        if not event_occured:
            self.get_logger().info('Service call failed: timeout')

            return None
        else:
            return future.result()
    
    def remove_null_values_and_keys(self, d):
        if isinstance(d, dict):
            return {k: self.remove_null_values_and_keys(v) for k, v in d.items() if v is not None} # Outcommented to use for few-shot examples: and k not in ['id', 'type']}
        elif isinstance(d, list):
            return [self.remove_null_values_and_keys(v) for v in d if v is not None]
        else:
            return d
 
    def reorder_keys(self, d):
        if isinstance(d, dict):
            keys_order = ['role', 'content', 'tool_calls']
            return {k: d[k] for k in keys_order if k in d}
        return d   
    
    def log_conversation(self, llm_response, log_file_path=None):
        """Log function to save the LLM responses to a file"""
        if log_file_path is None:
            log_file_path = self.conversation_log_file

        with open(log_file_path, 'a') as log_file:
            response = self.remove_null_values_and_keys(llm_response)
            response = self.reorder_keys(response)
            formatted_response = json.dumps(response, indent=4)
            formatted_response = formatted_response.replace('\\n', '\n')
            log_file.write(formatted_response)
            log_file.write('\n\n')

    def run_service_request(self, timeout=60):
        try:
            rclpy.spin_until_future_complete(self, self.future, timeout_sec=timeout)
            if self.future.result() is not None:
                return self.future.result()
            else:
                self.get_logger().error('Service call timed out')
                return "Service call time out"
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            return f"Service call failed: {e}"

    # Function to encode the image
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    # Convert state_snapshot to a JSON-serializable format
    def serialize_message(self, message):
        if isinstance(message, SystemMessage):
            return {"type": "SystemMessage", "content": message.content}
        elif isinstance(message, HumanMessage):
            return {"type": "HumanMessage", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"type": "AIMessage", "content": message.content, "tool_calls": message.tool_calls, "name": message.name}
        elif isinstance(message, ToolMessage):
            return {"type": "ToolMessage", "content": message.content, "name": message.name, "tool_call_id": message.tool_call_id}
        return message  # Default case for other types
    
    def save_snapshot(self):
        # Get current time and date from OS and format it for log file differentiation
        self.current_time = os.popen('date +"%Y-%m-%d_%H-%M-%S"').read().strip()

        # Save the current state snapshot of the sim_workflow_manager app to a file
        state_snapshot_file = self.conversation_log_folder + f"/state_snapshot_{self.current_time}.json"
        snapshot = self.sim_workflow_manager.get_state(self.sim_config).values

        serializable_snapshot = {
            key: [self.serialize_message(msg) for msg in value] if isinstance(value, list) else value
            for key, value in snapshot.items()
        }

        with open(state_snapshot_file, 'w') as file:
            formatted_response = json.dumps(serializable_snapshot, indent=4)
            formatted_response = formatted_response.replace('\\n', '\n')
            file.write(formatted_response)
            file.write('\n\n')
            #json.dump(serializable_snapshot, file, indent=4)

        self.get_logger().info(f"State snapshot saved to {state_snapshot_file}")
    
    def get_cam2world_transform(self):
        """Get the transformation matrix from camera to gripper coordinates."""        
        if load_use_sim():           
            # Works with 45 degree angle
            T_cam_world = np.array([
                                        [-1.0, -0.0,  0.0,  0.425],
                                        [-0.0,  np.cos(np.pi/4),  -np.cos(np.pi/4), 0.84],
                                        [-0.0,  -np.cos(np.pi/4),  -np.cos(np.pi/4), 0.65],
                                        [ 0.0,  0.0,  0.0,  1.0]
                                    ])
                 
        else:
            T_cam_world = np.array([
                [-0.999997441,  0.000171622184, -0.00225565295,  0.536974339],
                [ 0.00178189958,  0.674050369, -0.738683237,  0.992486794],
                [ 0.00139364928, -0.738685367, -0.674048950,  0.636035468],
                [ 0,                 0 ,             0 ,           1         ]
                ])

        return T_cam_world
        
    #@tool
    def plan_robot_trajectory(self, pose: list, arm: str) -> PlanMoveCommand.Response:
        """
        Plans a robot trajectory to a specified pose for a given arm. The planned trajectory is simulated 
        and visualized for the user. The trajectory can later be executed using the execute_planned_trajectory method.

        Args:
            pose (list): A list of 6 floating-point numbers representing the desired pose of the robot arm.
                         The first three numbers correspond to the x, y, z position in meters, and the last 
                         three numbers represent the roll, pitch, and yaw angles in degrees.
            arm (str): Specifies which arm to plan the trajectory for. Must be either 'left' or 'right'.

        Returns:
            PlanMoveCommand.Response: The response from the robot planning service, containing the result 
                                      of the trajectory planning process.
        Raises:
            ValueError: If the provided arm argument is not 'left' or 'right'.
            TimeoutError: If the planning service does not respond within the specified timeout period.

        Notes:
            - The function uses pre-calibrated transformation matrices to convert the pose from world 
              coordinates to MoveIt coordinates, depending on the selected arm.
            - The pose's orientation in roll, pitch, and yaw is converted to a quaternion format before 
              being sent to the planning service.
            - The function waits asynchronously for the planning service to respond, with a timeout of 75 seconds.
        """

        if arm == 'right':
            # Calibrated transformation matrix from world to moveit coordinates based on right arm
            T_world_moveit = np.array([ [ 0.99998383, -0.00168775,  0.00543034, -0.03063849],
                                        [ 0.00168078,  0.99999776,  0.00128864, -0.02827154],
                                        [-0.00543251, -0.00127949,  0.99998443,  0.8001058 ],
                                        [ 0.0,         0.0,         0.0,         1.0,      ] ])
            
        if arm == 'left':
            # Calibrated transformation matrix from world to moveit coordinates based on left arm
            T_world_moveit = np.array([ [ 0.99993911, -0.01089373,  0.00176324, -0.02348162],
                                        [ 0.01089142,  0.99993982,  0.00131455, -0.03821792],
                                        [-0.00177746, -0.00129526,  0.99999758,  0.80140745],
                                        [ 0.0,         0.0,         0.0,         1.0       ] ])
            
        
        # Extract the position from the pose and append 1 to make it a 4D vector
        pos_world = pose[:3]
        pos_world.append(1)

        # Transform the position from camera to world coordinates
        #pos_world = np.dot(T_world_cam, pos_cam)
        pos_moveit = np.dot(T_world_moveit, pos_world)

        rpy_world = pose[3:]
        quat_moveit = euler_to_quat(rpy_world)

        self.robot_plan_req.arm = arm
        self.robot_plan_req.position.x = float(pos_moveit[0])
        self.robot_plan_req.position.y = float(pos_moveit[1])
        self.robot_plan_req.position.z = float(pos_moveit[2])
        self.robot_plan_req.orientation.x = float(quat_moveit[1])
        self.robot_plan_req.orientation.y = float(quat_moveit[2])
        self.robot_plan_req.orientation.z = float(quat_moveit[3])
        self.robot_plan_req.orientation.w = float(quat_moveit[0])

        # Call the service asynchronously
        future = self.robot_plan_client.call_async(self.robot_plan_req)

        # Wait for the result
        response = self.wait_future(future, timeout=75)
        return response

    #@tool  
    def execute_planned_trajectory(self, arm: str) -> ExecuteMoveCommand.Response:
        """
        Executes a planned trajectory on the specified arm of the physical robot.

        This function sends a request to execute a trajectory that has been planned 
        using the `plan_robot_trajectory` function. It is important to ensure that 
        the `plan_robot_trajectory` function has been called prior to invoking this 
        function, as it relies on the trajectory data generated by the planning step.

        Args:
            arm (str): The identifier of the robot arm on which the trajectory 
                       should be executed (e.g., "left_arm" or "right_arm").

        Returns:
            ExecuteMoveCommand.Response: The response object containing the result 
                                         of the execution request, including success 
                                         status and any relevant feedback.

        Raises:
            TimeoutError: If the execution request does not complete within the 
                          specified timeout period (90 seconds).
        """

        self.robot_execute_req.arm = arm

        future = self.robot_execute_client.call_async(self.robot_execute_req)

        # Wait for the result
        response = self.wait_future(future, timeout=90)

        return response

    def switch_robot_mode(self, use_sim: bool) -> str:
        """
        Switch between simulation and physical robot mode.

        Args:
            use_sim (bool): If True, switch to simulation mode. If False, switch to real robot.

        Returns:
            str: A confirmation message indicating the mode change.
        """
        new_mode = set_use_sim(use_sim)
        self.use_sim = use_sim
        return f"Robot mode has been set to: {'simulation' if new_mode == 'True' else 'real robot'}."


    ########################################################################################
    # -------------------------- FUNCTIONS AVAILABLE TO THE LLM -------------------------- #
    ########################################################################################

    #@tool
    def detected_failure(self) -> bool:
        """Indicates that a failure has occurred in the system.

        This function is used to signal that an error or unexpected situation has been detected. 

        Returns:
            bool: True
        """
        self.get_logger().error("Failure detected")
        return True
    
    #@tool
    def detected_success(self) -> bool:
        """Indicates that a success has occurred in the system.

        This function is used to signal that a successful operation or event has been detected. 

        Returns:
            bool: True
        """
        self.get_logger().info("Success detected")
        return True

    #@tool
    def get_predefined_locations_and_poses(self) -> dict:
        """
        Retrieves a dictionary of predefined robot poses in world coordinates for specific locations.

        This function provides a mapping of predefined locations to their corresponding robot poses
        in world coordinates. It is intended for reference purposes only and does not perform any
        robot movement or pose adjustments.

        Returns:
            dict: A dictionary where keys represent predefined location names and values are the
            corresponding robot poses in world coordinates.
        """

        return self.coordinates

    #@tool   
    def find_object(self, object_name: str) -> GetObjectInfo.Response:
        """
        Uses the object detection service to locate and retrieve grasp poses for a specified object, 
        or if none of the specified object is found returns possible objects and thier center points.

        This method sends a service request to the object detector, providing the object name and a 4x4 transformation
        matrix (flattened) to convert camera coordinates to world coordinates.
         
        It receives a structured response containing detected objects with their 3D center points and possible grasp poses 
        (grasps only if the object was found). These are stored in a structured dictionary for easy access.

        Args:
            object_name (str): The name of the object to search for (e.g., "bottle", "book").

        Service returns:
            GetObjectInfo.Response: A response object that includes the number of detected objects and their grasp details.
            (objects found, center of object, 6D pose, grasp with). If no object is found, it returns the possible objects and their center points. 

        Function returns:
            -`self.objects_on_table` with structured grasp information in the following format:
            {
                'object_name i': {
                    'center_object': {x, y, z},
                    'grasps': {
                        'Top grasp': {
                            'center': {x, y, z},
                            'orientation': {roll, pitch, yaw},
                            'width': float
                        },
                        'grasp j': {
                            'center': {x, y, z},
                            'orientation': {roll, pitch, yaw},
                            'width': float
                        },
                        ...
                    }
                },
                ...
            }

        Notes:
            - Grasp orientation is stored in degrees (roll, pitch, yaw).
            - Each object is given a unique name (e.g., "bottle 0", "bottle 1") to avoid conflicts.
            - Requires the object detection service to be available and responsive.
        """
        
        # self.get_logger().info(f"\Requesting the Object detector service to find grasps for: {object_name}\n")

        # Call the object detection service, with the object name and the transformation matrix
        self.detector_req.object_name = object_name

        T = self.get_cam2world_transform()
        transform_msg = TransformMatrix()
        transform_msg.matrix = T.flatten().tolist()
        self.detector_req.transform = transform_msg

        future = self.detector_client.call_async(self.detector_req)

        # Wait for the result
        response = self.wait_future(future, timeout=125)

        # Check if the response is valid or if it timeouted
        if response is None:
            # self.get_logger().error("Failed to retrieve object detection response")
            return "Failed to retrieve object detection response. Make sure the object detection service is running."

        self.get_logger().info(f"\nObjects found: {response.object_count}\n")

        # Clear the previous objects
        self.objects_on_table = {}

        # For case where no object is found
        if response.object_count == 0:
            # self.get_logger().info(f"\nNo objects found. The possible objects information are saved in the response.\n")
            for i, detected_obj in enumerate(response.detected_objects):
                #object_name = detected_obj.name

                self.objects_on_table[detected_obj.name] = {
                    'center_object': {
                        'x': round(detected_obj.center_of_object.x,3),
                        'y': round(detected_obj.center_of_object.y,3),
                        'z': round(detected_obj.center_of_object.z,3)
                    }
                }
            
            return f"{object_name} could not be found. Instead YoloWorld found {response.object_count} objects. The possible objects are: {self.objects_on_table}"
        
        # For case where object is found
        else:
            # self.get_logger().info(f"\nNumber of objects found: {response.object_count}")

            for i, detected_obj in enumerate(response.detected_objects):
                object_name = detected_obj.name

                self.objects_on_table[object_name] = {
                    'centre_object': {
                        'x': round(detected_obj.center_of_object.x,3),
                        'y': round(detected_obj.center_of_object.y,3),
                        'z': round(detected_obj.center_of_object.z,3)
                    },
                    'size_object': {detected_obj.size_area},
                    'grasps': {}
                }

                # Debugging information
                # self.get_logger().info(f"Grasping poses: {detected_obj.grasps}")

                for j, grasp in enumerate(detected_obj.grasps):
                    
                    ##### rotate the grasp 90 degrees around the z-axis of the grasp
                    T_90z = np.eye(4)
                    # Define the rotation matrix for -90 degrees around the z-axis
                    R_90z = Rotation.from_euler('z', -90, degrees=True).as_matrix()
                    T_90z[:3, :3] = R_90z

                    R_W_G = Rotation.from_euler('xyz', [grasp.orientation.x, grasp.orientation.y, grasp.orientation.z], degrees=True).as_matrix()
                    pose = np.array([grasp.position.x, grasp.position.y, grasp.position.z])

                    # self.get_logger().info(f"Pose: {pose}")

                    T_W_G = np.eye(4)
                    T_W_G[:3, :3] = R_W_G
                    T_W_G[:3, 3] = pose
                    
                    if pose[2] > 0.04: # if center point is more than 3 cm above the table
                        T_90z[2,3] = 0.03 # move the grasp point 3 cm into the object
                    elif pose[2]>0.03: 
                        T_90z[2,3] = 0.02 
                    elif pose[2]>0.02: 
                        T_90z[2,3] = 0.0175
                    elif pose[2]>0.01:
                        T_90z[2,3] = 0.0075
                    elif pose[2]>0.0075:
                        T_90z[2,3] = 0.0035
                    elif pose[2]>0.005:
                        T_90z[2,3] = 0.0025
                    elif pose[2]>0.0025:
                        T_90z[2,3] = 0.0015
                    
                    T_new = T_W_G @ T_90z
                    pose_new = T_new[:3, 3]

                    roll, pitch, yaw = Rotation.from_matrix(T_new[:3,:3]).as_euler('xyz', degrees=True)
                    roll, pitch, yaw = [flip_if_near_180(a) for a in [roll, pitch, yaw]]

                    if pose_new[2] < 0.008:
                        pose_new[2] = 0.008

                    if j == 0:
                        grasp_name = 'Top down grasp'
                    else:
                        grasp_name = f'General grasp {j}'

                    self.objects_on_table[object_name]['grasps'][grasp_name] = {
                        'centre': {
                            'x': round(pose_new[0],3),
                            'y': round(pose_new[1],3),
                            'z': round(pose_new[2],3)
                        },
                        'orientation': {
                            'roll': round(roll,3),
                            'pitch': round(pitch,3),
                            'yaw': round(yaw,3)
                        }#,
                        #'width': round(grasp.grasp_width,3)
                    }
        # print(f"\nThe object detection service returned the following objects: {self.objects_on_table}\n")

        return self.objects_on_table
    
    #@tool
    def pick_up_object(self, pose: list, arm: str, object_width: int=0) -> bool:
        """
        Picks up an object by planning and executing a trajectory and closing the gripper.
        This function first opens the gripper, then plans a trajectory to an approach pose,
        executes the trajectory, closes the gripper to pick up the object, and finally lifts the object 10 cm
        to avoid collision when moving away. The function also handles the gripper width for the object.
        Args:
            pose (list): A list of 6 floating-point numbers representing the desired pose of the robot arm.
                         The first three numbers correspond to the x, y, z position in meters, and the last 
                         three numbers represent the roll, pitch, and yaw angles in degrees.
            arm (str): Specifies which arm to use ('left' or 'right').
            object_width (int, optional): Width of the object to grip in millimeters. Defaults to 0 mm.
            
        Returns:
            bool: True if the object was successfully picked up, False otherwise.
        """
        if len(pose) != 6:
            self.get_logger().error("Pose must be a list of 6 elements")
            return "Pose must be a list of 6 elements: [x, y, z, roll, pitch, yaw]"
        
        # First we calculate the approach pose
        T_approach = np.eye(4)
        T_approach[2, 3] = 0.05 # Place approach 5 cm along grasp z-axis

        R_pose = Rotation.from_euler('xyz', [pose[3], pose[4], pose[5]], degrees=True).as_matrix()
        T_pose = np.eye(4)
        T_pose[:3, :3] = R_pose
        T_pose[:3, 3] = pose[:3]

        # Convert the pose to the correct coordinate system
        T_pose = np.dot(T_pose, T_approach)

        # print(f"Old pose to pick up object: {pose}")

        # Now convert back to x, y, z, roll, pitch, yaw
        x, y, z = T_pose[:3, 3]
        roll, pitch, yaw = Rotation.from_matrix(T_pose[:3, :3]).as_euler('xyz', degrees=True)

        pose_approach = [x, y, z, roll, pitch, yaw]
        pose_depart = pose.copy()
        pose_depart[2] += 0.1 # Move up 10 cm

        # print(f"New pose to pick up object: {pose}")

        # First make sure the gripper is open
        if arm == 'left':
            gripper_response = self.manipulate_left_gripper(width=85)
        else:
            gripper_response = self.manipulate_right_gripper(width=167)

        if gripper_response is None or not gripper_response.success:
            self.get_logger().error("Failed to open gripper")
            return gripper_response # Previously returned: "Failed to open gripper"
        
        # Now plan the movement to the approach pose
        plan_response = self.plan_robot_trajectory(pose_approach, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan approach trajectory, it is possible the grasp is too low, consider moving it up 0.01")
            return plan_response # Previously returned: "Failed to plan approach trajectory"
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute approach trajectory")
            return execute_response # Previously returned: "Failed to execute approach trajectory"
        
        # Now plan the movement to the pose
        if load_use_sim(): 
            if arm == 'left':
                if pose[2] >= 0.03:  # if center point is more than 3 cm above the table
                    pose[2] -= 0.025  # Move down 2 cm for both grippers
                elif pose[2] < 0.03:
                    pose[2] = 0.001 # was 0.01
                #elif pose[2] < 0.02:
                #    pose[2] = 0.08
            else:
                if pose[2] >= 0.045:  # if center point is more than 3 cm above the table
                    pose[2] -= 0.02  # Move down 2 cm for both grippers
                elif pose[2] < 0.045:
                    pose[2] = 0.015 # was 0.022
                #elif pose[2] < 0.02:
                #    pose[2] = 0.01

        plan_response = self.plan_robot_trajectory(pose, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return plan_response # Previously returned: "Failed to plan grasp trajectory"
        
        # Execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return execute_response # Previously returned: "Failed to execute grasp trajectory"

        # Close the gripper
        # As width estimation is not accurate, we set width to 0 to make sure object is grasped
        if arm == 'left':
            gripper_response = self.manipulate_left_gripper(width=0)
        else:
            gripper_response = self.manipulate_right_gripper(width=0)

        if gripper_response is None or not gripper_response.success:
            self.get_logger().error("Failed to close gripper, consider grasping a bit higher up")
            return gripper_response # Previously returned: "Failed to close gripper"
        
        # At last lift the object to avoid collision when moving away
        plan_response = self.plan_robot_trajectory(pose_depart, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return plan_response # Previously returned: "Failed to plan grasp trajectory"
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return execute_response # Previously returned: "Failed to execute grasp trajectory"
        
        # Add a check for if object was grasped successfully
        if arm == 'left' and load_use_sim():
            angle = 45 * (80 / 85) / 180.0 * 3.14  # Degrees to radians
            joint_name = "left_2f_robotiq_85_left_knuckle_joint"

            POSITION_TOLERANCE = 0.1
            within_tolerance = False

            actual = self._2f_joint_values_mock[0]
            error = abs(actual - angle)

            self.get_logger().info(
                f"2F Joint {joint_name} | Target: {angle:.3f} | Actual: {actual:.3f} | Error: {error:.4f}"
            )

            gripper_response.success = False
            self.left_gripper_state = "Closed, not holding object. Consider moving the arm away and seach for the object again"
            if error > POSITION_TOLERANCE:
                within_tolerance = True
                gripper_response.success = True
                self.left_gripper_state = "Holding object"

            if not within_tolerance:
                self.get_logger().error("Failed to grasp object with left gripper")
                return "Failed to grasp object with left gripper."
            if within_tolerance:
                self.get_logger().info("Object picked up successfully with left gripper")

        elif arm == 'right' and load_use_sim():
            angle_1 = 65 * 1 / 180.0 * 3.14
            joint_name = "a_3f_finger_middle_joint_1"

            POSITION_TOLERANCE = 0.1
            within_tolerance = False

            actual = self._3f_joint_values_mock[4] # This is the middle finger joint 1 value
            error = abs(actual - angle_1)

            self.get_logger().info(
                f"3F Joint {joint_name} | Target: {angle_1:.3f} | Actual: {actual:.3f} | Error: {error:.4f}"
            )
            
            gripper_response.success = False
            self.right_gripper_state = "Closed, not holding object. Consider moving the arm away and seach for the object again"

            if error > POSITION_TOLERANCE:
                within_tolerance = True
                gripper_response.success = True
                self.right_gripper_state = "Holding object"
        
            if not within_tolerance:
                self.get_logger().error("Failed to grasp object with right gripper")
                return "Failed to grasp object with right gripper"
            if within_tolerance:
                self.get_logger().info("Object picked up successfully with right gripper")

        #if arm == 'left':
        #    gripper_response = self.manipulate_left_gripper(width=0)
        #else:
        #    gripper_response = self.manipulate_right_gripper(width=0)

        #if gripper_response is None or not gripper_response.success:
        #    self.get_logger().error("Failed to close gripper")
        #    return gripper_response # Previously returned: "Failed to close gripper"
        
        return "Object picked up successfully"
    
    #@tool
    def drop_off_object_at_pose(self, pose: list, arm: str) -> bool:
        """
        Drops off an object by planning and executing a trajectory and opening the gripper.
        This function first plans a trajectory to an approach pose, executes the trajectory,
        moves to the drop-off pose, opens the gripper to release the object, and finally moves
        the arm to its home position to avoid collision.
        Args:
            pose (list): A list of 6 floating-point numbers representing the desired pose of the robot arm.
                 The first three numbers correspond to the x, y, z position in meters, and the last 
                 three numbers represent the roll, pitch, and yaw angles in degrees.
            arm (str): Specifies which arm to use ('left' or 'right').
            
        Returns:
            bool: True if the object was successfully dropped off, False otherwise.
        """
        if len(pose) != 6:
            self.get_logger().error("Pose must be a list of 6 elements")
            return "Pose must be a list of 6 elements: [x, y, z, roll, pitch, yaw]"
        
        # First we calculate the approach pose
        T_approach = np.eye(4)
        T_approach[2, 3] = 0.08 # Place approach 5 cm along grasp z-axis

        R_pose = Rotation.from_euler('xyz', [pose[3], pose[4], pose[5]], degrees=True).as_matrix()
        T_pose = np.eye(4)
        T_pose[:3, :3] = R_pose
        T_pose[:3, 3] = pose[:3]

        # Convert the pose to the correct coordinate system
        T_pose = np.dot(T_pose, T_approach)
        pose_depart = pose.copy()
        pose_depart[2] += 0.1 # Move up 10 cm

        # print(f"Old pose to pick up object: {pose}")

        # Now convert back to x, y, z, roll, pitch, yaw
        x, y, z = T_pose[:3, 3]
        roll, pitch, yaw = Rotation.from_matrix(T_pose[:3, :3]).as_euler('xyz', degrees=True)

        pose_approach = [x, y, z, roll, pitch, yaw]
        
        # Now plan the movement to the approach pose
        plan_response = self.plan_robot_trajectory(pose_approach, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan approach trajectory")
            return plan_response # Previously returned: "Failed to plan approach trajectory"
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute approach trajectory")
            return execute_response # Previously returned: "Failed to execute approach trajectory"

        plan_response = self.plan_robot_trajectory(pose, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return plan_response # Previously returned: "Failed to plan grasp trajectory"
        
        # Execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return execute_response # Previously returned: "Failed to execute grasp trajectory"

        # Open the gripper
        if arm == 'left':
            gripper_response = self.manipulate_left_gripper(width=85)
        else:
            gripper_response = self.manipulate_right_gripper(width=167)

        if gripper_response is None or not gripper_response.success:
            self.get_logger().error("Failed to close gripper")
            return gripper_response # Previously returned: "Failed to close gripper"
        
        # lift the object to avoid collision when moving away
        plan_response = self.plan_robot_trajectory(pose_depart, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return plan_response # Previously returned: "Failed to plan grasp trajectory"
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return execute_response # Previously returned: "Failed to execute grasp trajectory"
        
        # Move the arm to home position
        if arm == 'left':
            pose_home = [1, 0.15, 0.3, 0, 0, 0]
        else:
            pose_home = [0, 0.15, 0.3, 0, 0, 0]

        # First plan the movement to the pose
        plan_response = self.plan_robot_trajectory(pose_home, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return plan_response # Previously returned: "Failed to plan grasp trajectory"
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return execute_response # Previously returned: "Failed to execute grasp trajectory"
        
        return "Object dropped off successfully"

    def move_to_pose(self, pose: list, arm: str) -> bool:
        """
        Moves the specified robotic arm to the given pose.
        Args:
            pose (list): Target pose for the robotic arm.
            arm (str): Identifier for the arm to be moved.
        Returns:
            bool: True if the movement was successful, False otherwise.
        """

        # First plan the movement to the pose
        plan_response = self.plan_robot_trajectory(pose, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan trajectory")
            return plan_response
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute trajectory")
            return execute_response
        
        return True

    #@tool
    def manipulate_right_gripper(self, width: int=167, speed: int=110, force: int=15) -> Robotiq3FGripperOutputService.Response:  # Defaults to open gripper with max speed and minimum force
        """
        Adjusts the right gripper's position, speed, and force.

        This function controls the right gripper of the robot, allowing it to open, close, 
        or adjust to a specific width. The speed and force of the gripper can also be customized. 
        It is important to note that this function executes immediately and should not be called 
        simultaneously with trajectory planning functions. For pickup tasks, ensure that this 
        function is called only after executing a trajectory.

        Parameters:
            width (int, required): The desired width of the right gripper in millimeters [mm]. 
                         The range is 0-167, where 0 is fully closed and 167 is fully open. 
                         Default is 167.
            speed (int, optional): The speed of the gripper in millimeters per second [mm/sec]. 
                         The range is 22-110, where 22 is the minimum speed and 110 is the maximum speed. 
                         Default is 110.
            force (int, optional): The gripping force in Newtons [N]. 
                         The range is 15-60, where 15 is the minimum force and 60 is the maximum force. 
                         Default is 15.

        Returns:
            response: The response from the asynchronous service call to control the gripper. 
                      If the input parameters exceed the gripper's capabilities, an error message 
                      is logged, and a corresponding error string is returned.

        Raises:
            None: This function does not raise exceptions but logs errors if the input parameters 
                  are out of the valid range.

        Notes:
            - Ensure the input parameters are within the specified ranges to avoid errors.
            - This function directly interacts with the gripper controller and sends the 
              appropriate commands to adjust the gripper's behavior.
            - The function waits for the service call to complete with a timeout of 15 seconds.
        """
        if width < 0 or width > 167:
            self.get_logger().error('Requested right gripper width exceeds gripper capabilities')
            return 'Requested gripper width exceeds gripper capabilities'
        if speed < 22 or speed > 110:
            self.get_logger().error('Requested right gripper speed exceeds gripper capabilities')
            return 'Requested right gripper speed exceeds gripper capabilities'
        if force < 15 or force > 60:
            self.get_logger().error('Requested right gripper force exceeds gripper capabilities')
            return 'Requested right gripper force exceeds gripper capabilities'
        
        # Adjust the gripper width to ensure secure grasping
        """
        if width < 10:
            width = 0
        elif width == 167:
            pass
        else:
            width = width - 10
        """

        # Rviz gripper 
        self._gripper_req.width = float(width)   
        self._gripper_req.gripper_name = "3f"

        

        if load_use_sim():
            future2 = self._gripper_client.call_async(self._gripper_req)
            response2 = self.wait_future(future2, timeout=15)
            
            while(response2 == None):
                self.get_logger().info(f"Gripper response failed, trying agian")

                future2 = self._gripper_client.call_async(self._gripper_req)
                response2 = self.wait_future(future2, timeout=15)
                
                self.get_logger().info(f"Gripper response is: {response2}")

            if width == 167:
                self.get_logger().info("Gripper opened")
                response2.log = "Gripper opened"
                response2.success = True
                self.right_gripper_state = "Open"
            elif response2.success is False and response2.log == "3f gripper move failed":
                self.get_logger().error("Gripper failed to plan")
                response2.log = "Gripper failed to plan close movement, try picking up 0.005 higher up."
                response2.success = False
                self.right_gripper_state = "Open"
            elif response2.success is False:
                self.get_logger().info("Gripper succesfully grasped object")
                response2.log = "Gripper succesfully grasped object"
                response2.success = True
                self.right_gripper_state = "Holding object"
            else:
                self.get_logger().error("Gripper failed to grasp object")
                response2.log = "Gripper did not detect any object when closing, make sure the object is still present."
                response2.success = False
                self.right_gripper_state = "Closed, holding no object"
            return response2
        else:
            self._3f_controller.output_registers.r_act = 1  # Active Gripper
            self._3f_controller.output_registers.r_mod = 1  # Basic Gripper Mode
            self._3f_controller.output_registers.r_gto = 1  # Go To Position
            self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
            self._3f_controller.output_registers.r_pra = round((167 - width) / 167 * 112)          # Gripper limitations [0 - 167mm]
            self._3f_controller.output_registers.r_spa = round((speed - 22) / (110 - 22) * 255)    # Speed limitations [22 - 110mm/sec]
            self._3f_controller.output_registers.r_fra = round((force - 15) / (60 - 15) * 255)     # Force limitations [15 - 60N]

            # Call the service asynchronously
            future1 = self._3f_controller_cli.call_async(self._3f_controller)

            response1 = self.wait_future(future1, timeout=15)

            if self._3f_input_registers.g_sta == 1 or self._3f_input_registers.g_sta == 2:
                self.get_logger().info("Gripper succesfully grasped object")
                response1.log = "Gripper succesfully grasped object"
                response1.success = True
                self.right_gripper_state = "Holding object"
            elif width == 167:
                self.get_logger().info("Gripper opened")
                response1.log = "Gripper opened"
                response1.success = True
                self.right_gripper_state = "Open"
            else:
                self.get_logger().error("Gripper failed to grasp object")
                response1.log = "Gripper did not detect any object when closing, make sure the object is still present."
                response1.success = False
                self.right_gripper_state = "Closed, holding no object"

            return response1


    #@tool
    def manipulate_left_gripper(self, width: int=85, speed: int=110, force: int=70) -> Robotiq2F85GripperCommand.Response:   # Defaults to open gripper with fast speed and minimum force
        """
        Adjusts the left gripper's width, speed, and force to open, close, or position it at an intermediate state.

        This function allows precise control of the left gripper by specifying the desired width, speed, and force. 
        The gripper's width determines how far it opens or closes, while speed and force control the movement's 
        velocity and strength, respectively. The function validates the input parameters to ensure they are within 
        the gripper's operational limits.

        Parameters:
            width (int, required): The desired width of the left gripper in millimeters [mm]. 
                Must be between 0 (fully closed) and 85 (fully open). Default is 85.
            speed (int, optional): The movement speed of the left gripper in millimeters per second [mm/sec]. 
                Must be between 20 and 150. Default is 110.
            force (int, optional): The gripping force in Newtons [N]. 
                Must be between 20 and 235. Default is 20.

        Returns:
            response: The result of the gripper command execution. If the input parameters are invalid, 
                an error message is logged and returned.

        Notes:
            - This function executes the gripper command immediately. Do not call it alongside 
              `plan_robot_trajectory` expecting it to execute as part of a trajectory plan.
            - Ensure the input parameters are within the specified ranges to avoid errors.
        """

        # The real gripper 
        if width < 0 or width > 85:
            self.get_logger().error(f' WIDTH: {width}')
            self.get_logger().error('Requested left gripper width exceeds gripper capabilities')
            return 'Requested gripper width exceeds gripper capabilities'
        if speed < 20 or speed > 150:
            self.get_logger().error('Requested left gripper speed exceeds gripper capabilities')
            return 'Requested right gripper speed exceeds gripper capabilities'
        if force < 20 or force > 235:
            self.get_logger().error('Requested left gripper force exceeds gripper capabilities')
            return 'Requested right gripper force exceeds gripper capabilities'

        # Rviz gripper
        self._gripper_req.width = float(width)   # Opening in millimeters. Must be between 0 and 85 mm.
        self._gripper_req.gripper_name = "2f"

        # Wait for the result
        if load_use_sim():
            self.get_logger().info("Simulated gripper command sent")
            future2 = self._gripper_client.call_async(self._gripper_req)
            response2 = self.wait_future(future2, timeout=15)
            if width == 85:
                self.get_logger().info("Gripper opened")
                response2.log = "Gripper opened"
                response2.success = True
                self.left_gripper_state = "Open"
            elif response2.success is False and response2.log == "2f gripper move failed":
                self.get_logger().info("Gripper could not plan close")
                response2.log = "Left gripper failed to plan close movement, try picking up 0.005 higher up."
                response2.success = False
                self.left_gripper_state = "Open"
            elif response2.success is False:
                self.get_logger().info("Gripper succesfully grasped object")
                response2.log = "Gripper succesfully grasped object"
                response2.success = True
                self.left_gripper_state = "Holding object"
            else:
                self.get_logger().error("Gripper failed to grasp object")
                response2.log = "Gripper did not detect any object when closing, make sure the object is still present."
                response2.success = False
                self.left_gripper_state = "Closed, holding no object"
            return response2
        else:
            self._2f_req.width = float(width)   # Opening in millimeters. Must be between 0 and 85 mm.
            self._2f_req.speed = float(speed)   # Speed in mm/s. Must be between 20 and 150 mm/s.
            self._2f_req.force = float(force)   # Force in N. Must be between 20 and 235 N.

            # Publish command to left gripper
            future1 = self._2f_client.call_async(self._2f_req)

            self.get_logger().info("Real gripper command sent")

            response1 = self.wait_future(future1, timeout=15)

            if "An object was grasped." == response1.log:
                self.left_gripper_state = "Holding object"
                
            elif "Gripper is open." == response1.log:
                self.left_gripper_state = "Open"
                
            elif "Gripper did not detect any object when closing, make sure the object is still present." == response1.log:
                self.left_gripper_state = "Closed, holding no object"
                

            return response1
        
    def task_complete(self) -> bool:
        """
        If the task has been compeleted before the tool list is empty call this function to return to the user. 
        """
        
        return True
    
