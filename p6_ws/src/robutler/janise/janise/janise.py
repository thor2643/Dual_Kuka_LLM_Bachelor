# Import libraries
from openai import OpenAI
import ollama
import json
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import numpy as np
import readline
from threading import Event
import base64
import cv2
from cv_bridge import CvBridge, CvBridgeError
from scipy.spatial.transform import Rotation 
import math
from utils.mode_switch import load_use_sim, set_use_sim

# Langgraph / Langchain libraries
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.tools.base import StructuredTool

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

# ROS 2 libraries and Node structure
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
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
from robotiq_2f_85_interfaces.srv import Robotiq2F85GripperCommand
from project_interfaces.srv import GetImage
from project_interfaces.srv import GetSimCameraData
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Image

class LLMNode(Node):
    def __init__(self):
        super().__init__('minimal_client')

        client_cb_group = MutuallyExclusiveCallbackGroup()
        gui_service_cb_group = MutuallyExclusiveCallbackGroup()

        self.srv = self.create_service(
            PromptJanice, 'send_prompt', self.gui_handle_service, callback_group=gui_service_cb_group
        )
        self.get_logger().info('Service Server is ready.')

        # Gripper service client
        self._3f_controller = Robotiq3FGripperOutputService.Request()
        self._3f_controller_cli = self.create_client(Robotiq3FGripperOutputService, "Robotiq3FGripper/OutputRegistersService", callback_group=client_cb_group)

        self._2f_client = self.create_client(Robotiq2F85GripperCommand, 'gripper_2f_service', callback_group=client_cb_group)
        self._2f_req = Robotiq2F85GripperCommand.Request()

        # Moveit gripper client
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

        # Specify a specific microphone if needed
        self.microphone_index = 8
        self.microphone_timeout = 10

        # Decide whether to use Ollama API or OpenAI API
        self.use_ollama = False

        # Attributes
        self.future = 0
        self.llm_loop = False
        self.state = {}

        # Get current time and date from OS and format it for log file differentiation
        self.current_time = os.popen('date +"%Y-%m-%d_%H-%M-%S"').read().strip()
        self.get_logger().info(f"Current time and date: {self.current_time}")

        self.conversation_log_folder = 'src/robutler/janise/resource/conversation_logs'
        self.conversation_log_file = self.conversation_log_folder + f'/{self.current_time}.json'

        # Create the directory if it doesn't exist
        if not os.path.exists(self.conversation_log_folder):
            os.makedirs(self.conversation_log_folder)

        """
        # Create the JSON file if it doesn't exist
        if not os.path.exists(self.conversation_log_file):
            with open(self.conversation_log_file, 'w') as file:
                pass
        """

        # Define the locations in the environment
        self.coordinates = { # Predefined poses for different locations
            'HOME_RIGHT_ARM': {'x': '0.1', 'y': '0.3', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'},
            'HOME_LEFT_ARM': {'x': '0.9', 'y': '0.3', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'}
        }

        # Define the tools available to the LLM
        self.tools = [StructuredTool.from_function(self.get_predefined_locations_and_poses), 
                      StructuredTool.from_function(self.find_object),
                      StructuredTool.from_function(self.plan_robot_trajectory), 
                      StructuredTool.from_function(self.execute_planned_trajectory), 
                      StructuredTool.from_function(self.manipulate_right_gripper), 
                      StructuredTool.from_function(self.manipulate_left_gripper), 
                      StructuredTool.from_function(self.get_current_pose), 
                      StructuredTool.from_function(self.stop_message_looping)]
                
        self.tool_node = ToolNode(self.tools)

        # Initialize Ollama client or OpenAI client with API key and optional project ID
        if self.use_ollama:
            self.client = ollama.Client()
        else:
            # load the project id and key from json file
            with open('src/robutler/janise/API_KEY.json') as f:
                api_data = json.load(f)
            API_KEY = api_data['API_KEY']

            # Set API key
            if not os.environ.get("OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = API_KEY 

        # Initialise the model
        # Change this to the model you want to use
        self.model = ChatOpenAI(model="gpt-4o")
        self.bound_model = self.model.bind_tools(self.tools)
        self.think_model = self.model.bind_tools(self.tools, tool_choice='none') # Forced to not call any tools

        self.memory = MemorySaver()

        # Define a new graph
        # Using graphs allows us to define the flow of the conversation
        # To grasp this, it might be helpful to read a bit about graph theory
        # For each node action taken, we can will store the state of the conversation i.e. the messages
        self.workflow = StateGraph(MessagesState)

        # Define the two nodes we will cycle between
        # The action node is the node that can actually call the tool using langgraphs's ToolNode class
        # We could for an example also add an observation node for our evaluating model
        self.workflow.add_node("agent", self.call_model)
        self.workflow.add_node("action", self.tool_node)

        # Consider adding another system message for this model
        self.workflow.add_node("thought", self.think)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        # self.workflow.add_edge(START, "agent")
        self.workflow.add_edge(START, "thought")
        self.workflow.add_edge("thought", "agent")

        # We now add a conditional edge
        # This means that the edge taken is determined by the function passed in
        self.workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self.should_continue,
            # Next, we pass in the path map - all the possible nodes this edge could go to
            ["action", END],
        )

        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        self.workflow.add_edge("action", "thought")
        self.workflow.add_edge("thought", "agent")


        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        self.agent = self.workflow.compile(checkpointer=self.memory)

        # Comment in to save a png of the graph and show it
        """
        graph = self.agent.get_graph()

        # Display the workflow graph using OpenCV
        graph_image_path = f"{self.conversation_log_folder}/workflow_graph_{self.current_time}.png"
        graph.draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
            output_file_path=graph_image_path,
        )

        # Load and display the image using OpenCV
        try:
            graph_image = cv2.imread(graph_image_path)
            if graph_image is not None:
                cv2.imshow("Workflow Graph", graph_image)
                cv2.waitKey(0)  # Wait for a key press to close the window
                cv2.destroyAllWindows()
            else:
                self.get_logger().error("Failed to load the workflow graph image.")
        except ImportError:
            self.get_logger().error("OpenCV is not installed. Please install it to display the workflow graph.")

        """

        # Setting a thread_id helps the model remember the context of the conversation
        self.config = {"configurable": {"thread_id": "1"}}
        self.config_think = {"configurable": {"thread_id": "CoT1"}} # CoT = Chain of Thoughts

        self.initial_prompt_Janise = SystemMessage(content = """
            Your name is Janise. You are an AI robotic arm assistant for task reasoning and manipulation tasks.

            Context for your Workspace:
            - You operate in a dual-arm robotic cell consisting of two collaborative KUKA iiwa 7 robots, each with 7 degrees of freedom (DoF). Both robots are mounted on a fixed frame positioned on top of a table, which provides a stable working surface.
            - The setup includes a left and right side, each equipped with its respective robot arm:
                - The left arm is equipped with a RobotIQ 2F-85 gripper for precise, standard gripping tasks.
                - The right arm is equipped with a RobotIQ 3F gripper, offering more versatile grasping options. 
            - An Intel RealSense D435i depth camera is mounted on the left robot arm to view the workspace from its perspective, allowing for accurate depth perception and object detection on the table.

            Spatial and Coordinate Understanding:
            - Your workspace operates within a "world" coordinate system with its origin (0,0,0) located at the outermost right edge of the table (from the camera's viewpoint). The division of the workspdace can be considered as follows:
                - *Left side*: All x-values above 0.5.
                - *Right side*: All x-values below 0.5
                - *Front of table*: All y-values below 0.3
                - *Back of table*: All y-values above 0.3
                - *Middle of table*: All values near the specified value above
            - The table extends from 0.0 to 1.0 on the X-axis and from 0.0 to 0.67 on the Y-axis.
            - The grippers must never go below 0 in height as they will then collide with the table.


            Operational Instructions:
            - Given a user request you must perform the most appropriate action that you are capable.
            - Before you are to make decisions, another agent named Socrates will provide you with insights and guidance to ensure that the correct actions are taken. You should always consider the suggestions made by Socrates before making a decision.
            - If not specified by the user, use the left arm for operations on the left side and use the right arm for operations on the right side.
            - Perform steps in an appropriate order e.g. move arm to object before closing gripper and plan trajectory before executing it.
            - Never manipulate the grippers before the arms are moved to the desired position!! 
            - Close the gripper to 0 and not grasp_width for the object you must grasp.
            - Safety is of utmost importance, so when in doubt always consult the user first. Especially for actions that move the robot.
                  
        """)

        self.initial_prompt = [
            self.initial_prompt_Janise, #TODO get_available_objects does not ecxist anymore
            HumanMessage(content = "To which poses can the robot arm be moved?"),
            HumanMessage(content = "The robot arms can be moved to any positions within the workspace. However, there is a function available that provides predefined poses and locations. Janise should consider calling that.",
                      name = "Socrates"),
            AIMessage(content = "",
                      tool_calls = [{"name": "get_predefined_locations_and_poses", "args": {}, "id": "call_pTZTKZcHPTOPxDn3qnViIWWu"}],
                      name = "Janise"),
            ToolMessage(content = "{'HOME_RIGHT_ARM': {'x': '0.1', 'y': '0.3', 'z': '0.3', 'roll': '0', 'pitch': '0', 'yaw': '0'}, 'HOME_LEFT_ARM': {'x': '0.9', 'y': '0.3', 'z': '0.3', 'roll': '0', 'pitch': '0', 'yaw': '0'}",
                        tool_call_id = "call_pTZTKZcHPTOPxDn3qnViIWWu"),
            HumanMessage(content = "The function returns valid predefined poses for the robot arms. As this was all that was requested, Janise should now return this information to the user."),
            AIMessage(content = """The robot arms can be moved to several predefined poses. Here are some of the poses:

                    1. **Home Position for Right Arm**:
                    - Coordinates: (0.1, 0.3, 0.3)
                    - Orientation: roll 0\u00b0, pitch 0\u00b0, yaw 0\u00b0

                    2. **Home Position for Left Arm**:
                    - Coordinates: (0.9, 0.3, 0.3)
                    - Orientation: roll 0\u00b0, pitch 0\u00b0, yaw 0\u00b0

                    Should you desire to move one of the arms to one of these positions, feel free to let me know.""",
                    name = "Janise"),
            HumanMessage(content = "What objects can you find?"),
            HumanMessage(content = "To answer this Janise should consider the available functions. The function \"get_available_objects\" returns predefined objects that can be detcted. This seems like an appropriate function to call.",
                      name = "Socrates"),
            AIMessage(content = "",
                      tool_calls = [{"name": "get_available_objects", "args": {}, "id": "call_KZ4pgcOBYotzY1QERRB0OiFn"}],
                      name = "Janise"),
            ToolMessage(content = "['red_brick', 'green_brick', 'yellow_brick', 'orange_brick', 'blue_brick', 'pink_brick', 'light_blue_brick', 'light_green_brick', 'purple_brick']",
                        tool_call_id = "call_KZ4pgcOBYotzY1QERRB0OiFn"),
            HumanMessage(content = "The returned objects are the predefined objects that can be detected. Janise should now return this information to the user.",
                      name = "Socrates"),
            AIMessage(content = """I am able to locate the following objects within the workspace:

                    - Red Brick
                    - Green Brick
                    - Yellow Brick
                    - Orange Brick
                    - Blue Brick
                    - Pink Brick
                    - Light Blue Brick
                    - Light Green Brick
                    - Purple Brick

                    If you need assistance with any of these objects, please let me know.""",
                    name = "Janise")
            ]
        
        self.initial_prompt_CoT = SystemMessage(content = """Your name is Socrates. You act as a critical thinker and must help the other LLM agent Janise to take proper action based on a user's request. 
                                                                You are to provide short and precise reasoning and guidance to Janise to ensure that the correct actions are taken. Your message is appended to the conversation for Janise to consider.
                                                                As Janise is controlling a dual arm robot you must provide her with insights to the physical world, while considering the robot's capabilities and limitations.
                                                                You are NOT allowed to call any tools yourself and can therefore only make suggestions for Janise to consider. You should always provide reasoning for your suggestions.
                                                                You are set to make suggestions to Janise after an incoming user request or after a tool call has returned.
                                                                You are never answering directly to the user, but only to Janise. Therefore, never take "you" in the user's request as if the user is talking to you. Janise is the only model communicating with the user.
                                                 
                                                                To help you reason better you are given an image of the workspace. This you can use to provide better guidance to Janise.

                                                                Also apply your guidance in the context of the user request. You are to ensure that the overarching goal is not forgotten.
                                                                """)
        

        # Append the initial prompt to the message state
        self.agent.update_state(self.config, {"messages": self.initial_prompt})


    ##############################################################################
    # -------------------------- SPEECH FUNCTIONALITY -------------------------- #
    ##############################################################################


    def speech_to_text(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                self.get_logger().info("Listening for speech...")
                audio = recognizer.listen(source, timeout=self.microphone_timeout)

            try:
                text = recognizer.recognize_google(audio)
                self.get_logger().info(f"Recognized speech: {text}")
                return text
            except sr.UnknownValueError:
                self.get_logger().error("Could not understand audio")
                return "Error: Could not understand audio."
            except sr.RequestError as e:
                self.get_logger().error(f"Google Speech Recognition error: {e}")
                return f"Error: {e}"
        except sr.WaitTimeoutError:
            self.get_logger().error("Microphone input timed out")
            return "Error: Microphone input timed out."
        except Exception as e:
            self.get_logger().error(f"Failed to capture audio: {e}")
            return "Error: Failed to capture audio."

    def text_to_speech(self, text):
        self.get_logger().info(f"Converting text to speech: {text}")
        try:
            unique_filename = f"output_{os.getpid()}.mp3"
            tts = gTTS(text=text, lang='en')
            tts.save(unique_filename)
            playsound(unique_filename)
            os.remove(unique_filename)
        except Exception as e:
            self.get_logger().error(f"Failed to convert text to speech: {e}")


    #######################################################################################
    # --------------------------------- EXTRA FUNCTIONS --------------------------------- #
    #######################################################################################

    def convert_to_color_img(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            color_img_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR by default)
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting color image: {e}')

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

    def euler_to_quat(self, euler_angles):
        cr = np.cos(np.deg2rad(euler_angles[0]) * 0.5)
        sr = np.sin(np.deg2rad(euler_angles[0]) * 0.5)
        cp = np.cos(np.deg2rad(euler_angles[1]) * 0.5)
        sp = np.sin(np.deg2rad(euler_angles[1]) * 0.5)
        cy = np.cos(np.deg2rad(euler_angles[2]) * 0.5)
        sy = np.sin(np.deg2rad(euler_angles[2]) * 0.5)

        q_w = cr * cp * cy + sr * sp * sy
        q_x = sr * cp * cy - cr * sp * sy
        q_y = cr * sp * cy + sr * cp * sy
        q_z = cr * cp * sy - sr * sp * cy

        return [q_w, q_x, q_y, q_z]
    
    def quat_to_euler(self, quat):
        w, x, y, z = quat
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = np.degrees(np.arctan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = np.degrees(np.arcsin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = np.degrees(np.arctan2(t3, t4))

        return [roll, pitch, yaw]

    def update_current_state(self):
        """Retrieve the current state of the Robot cell, which can be fed as observation to the LLM
        
        Returns:
            dict: The current state of the Robot cell
        """

        self.state = {
            'left_gripper': {
                'width': 85,
            },
            'right_gripper': {
                'width': 155, # 167 before but thats wrong
            },
            'services_unavailable': None,
        }
    
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

        # Save the current state snapshot of the agent app to a file
        state_snapshot_file = self.conversation_log_folder + f"/state_snapshot_{self.current_time}.json"
        snapshot = self.agent.get_state(self.config).values

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
    
    def convert_to_transformation_matrix(self, rotation, translation):
        """
        Converts a rotation matrix and translation vector into a 4x4 transformation matrix.
        """
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = np.array(rotation)
        transformation_matrix[:3, 3] = np.array(translation).flatten()
        return transformation_matrix
    
    def get_cam2world_transform(self):
        """Get the transformation matrix from camera to gripper coordinates."""
        T_cam_gripper = np.array([
            [-0.0687947, -0.99762731, -0.00265413, 0.09516971],
            [-0.99743676, 0.06883355, -0.01954097, 0.03406203],
            [0.0196773, 0.00130301, -0.99980553, 0.15210002],
            [0.0, 0.0, 0.0, 1.0]
        ])

        # Get gripper pose (try a few times if not successful)
        for i in range(5):
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

                t_gripper_moveit =  [
                    transform_3.transform.translation.x,
                    transform_3.transform.translation.y,
                    transform_3.transform.translation.z
                ]

                R_gripper_moveit = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=True).as_matrix()
                T_gripper_moveit = self.convert_to_transformation_matrix(R_gripper_moveit, t_gripper_moveit)
                self.get_logger().info("Succefully got gripper pose")

                break

            except tf2_ros.LookupException:
                if i < 4:
                    self.get_logger().info("Retrying...")
                    #rclpy.spin_once(self, timeout_sec=0.1)
                else:
                    self.get_logger().error("Failed to get gripper pose after multiple attempts")

        T_moveit_world = np.array([
            [0.99993911, 0.01089142, -0.00177746, 0.02532091],
            [-0.01089373, 0.99993982, -0.00129526, 0.03899785],
            [0.00176324, 0.00131455, 0.99999758, -0.80131387],
            [0., 0., 0., 1.]
        ])

        T_cam_world = T_moveit_world @ T_gripper_moveit @ T_cam_gripper 

        return T_cam_world

    def request_rvis_image(self):
        """Implemented workaround to get a screenshot of the RViz GUI using the GetImage service.
        Used to simulate a camera image for the object detection service."""
        self.get_image_req.execute = True
        future = self.get_image_client.call_async(self.get_image_req)

        # Wait for the result
        response = self.wait_future(future, timeout=10)

        if response is not None:
            image = self.bridge.imgmsg_to_cv2(response.image, desired_encoding='bgr8')

            cv2.imwrite("image.jpg", image)

            return image
        else:
            self.get_logger().error("Failed to retrieve image from RViz")
            return None


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

    #######################################################################################
    # ------------------------------ LANGGRAPH FUNCTIONS -------------------------------- #
    #######################################################################################

    # If a tool is to be called, the action node is called otherwise the agent node is called
    def should_continue(self, state: MessagesState):
        """Return the next node to execute."""
        last_message = state["messages"][-1]
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return END
        # Otherwise if there is, we continue
        return "action"
    
    # This is a simple helper function to filter the messages
    # Modify this to fit your use case or use off-the-shelf tools from langchain_core
    def filter_messages(self, messages: list):
        # This is very simple helper function which only ever uses the last message
        return messages[-1:]
    
    # Define the function that calls the model
    # Takes in the cureent message history and returns the response
    def call_model(self, state: MessagesState):
        # We append the initial prompt to Janise
        state["messages"][0] = self.initial_prompt_Janise

        # Append the initial prompt to the message state
        self.agent.update_state(self.config, {"messages": state["messages"]})

        response = self.bound_model.invoke(state["messages"])
        # We return a list, because this will get added to the existing list
        response.name = "Janise"
        return {"messages": response}
    
    def think(self, state: MessagesState):
        # We append an image to the CoT message
        #image_path = "image.jpg"

        # Resize the image to 524x524
        # Change this to get the actual image from the camera
        #original_image = cv2.imread(image_path)
        if load_use_sim():
            for i in range(5):
                request = GetSimCameraData.Request()
                future = self.sim_cam_client.call_async(request)

                # Wait for the result
                response = self.wait_future(future, timeout=5)

                if response is not None:
                    response = future.result()

                    color_img_rgb = self.bridge.imgmsg_to_cv2(response.color_image, desired_encoding="rgb8")
                    self.color_img_sim = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)
                    original_image = self.color_img_sim
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
        image = self.encode_image(resized_image_path)

        message = HumanMessage(
            content=[
                {"type": "text", "text": """Here is an overview of the workspace. Please provide guidance to Janise based on this image.
                """},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}",},
                },
            ]
        )

        # We must replace the system message for Janise with the system message for Sokrates
        state["messages"][0] = self.initial_prompt_CoT
        state["messages"].append(message)

        # But it cannot analyze the image and the chat history at the same time
        response_2 = self.think_model.invoke(state["messages"])

        # Delete the image from history to save tokens
        state["messages"].pop()

        # Convert to Human message, such that Janise does not think she answered herself.
        response_human = HumanMessage(content=response_2.text())
        response_human.name = "Socrates"

        # We return a list, because this will get added to the existing list
        return {"messages": response_human}
    

    ########################################################################################
    # -------------------------- FUNCTIONS AVAILABLE TO THE LLM -------------------------- #
    ########################################################################################

    #@tool
    def stop_message_looping(self) -> str:
        """ Disables the message looping mechanism used for sequential function calls.

        This function is essential when multiple function calls are chained together, 
        where the output of one function serves as the input for the next. By default, 
        message looping is enabled, allowing seamless execution of such chains without 
        requiring user intervention after each step.

        Once all necessary function calls are completed, this function should be invoked 
        to disable the message looping. This ensures that a final response is generated 
        and sent to the user, signaling the end of the process and awaiting the next command.

        Returns:
            str: A confirmation message indicating that message looping has been disabled.
        """
        self.llm_loop = False

        print("\nMessage looping has been disabled.")

        return "Message looping has been disabled."  

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
        
        self.get_logger().info(f"\Requesting the Object detector service to find grasps for: {object_name}\n")

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
            self.get_logger().error("Failed to retrieve object detection response")
            return None

        self.get_logger().info(f"\nObjects found: {response.object_count}\n")

        # For case where no object is found
        if response.object_count == 0:
            self.get_logger().info(f"\nNo objects found. The possible objects information are saved in the response.\n")
            for i, detected_obj in enumerate(response.detected_objects):
                object_name = detected_obj.name

                self.objects_on_table[object_name] = {
                    'center_object': {
                        'x': detected_obj.center_of_object.x,
                        'y': detected_obj.center_of_object.y,
                        'z': detected_obj.center_of_object.z
                    }
                }
        # For case where object is found
        else:
            self.get_logger().info(f"\nNumber of objects found: {response.object_count}")

            self.objects_on_table = {}  # Reset table

            for i, detected_obj in enumerate(response.detected_objects):
                object_name = detected_obj.name

                self.objects_on_table[object_name] = {
                    'center_object': {
                        'x': detected_obj.center_of_object.x,
                        'y': detected_obj.center_of_object.y,
                        'z': detected_obj.center_of_object.z
                    },
                    'grasps': {}
                }

                for j, grasp in enumerate(detected_obj.grasps):
                    
                    # rotate the grasp 90 degrees around the z-axis of the grasp

                    # Define the rotation matrix for 90 degrees around the z-axis
                    R_90z = Rotation.from_euler('z', 90, degrees=True).as_matrix()
                    # Define grasp rotation matrix from World to Grasp coordinates
                    R_W_G = Rotation.from_euler('xyz', [grasp.orientation.x, grasp.orientation.y, grasp.orientation.z], degrees=True).as_matrix()
                    R_new = R_W_G @ R_90z
                    roll, pitch, yaw = Rotation.from_matrix(R_new).as_euler('xyz', degrees=True)

                    self.objects_on_table[object_name]['grasps'][f'grasp {j}'] = {
                        'center': {
                            'x': grasp.position.x,
                            'y': grasp.position.y,
                            'z': grasp.position.z
                        },
                        'orientation': {
                            'roll': roll,
                            'pitch': pitch,
                            'yaw': yaw
                        },
                        'width': grasp.grasp_width
                    }
        print(f"\nThe object detection service returned the following objects: {self.objects_on_table}\n")

        return self.objects_on_table


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
        quat_moveit = self.euler_to_quat(rpy_world)

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

        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 1  # Basic Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = round((167 - width) / 167 * 112)          # Gripper limitations [0 - 167mm]
        self._3f_controller.output_registers.r_spa = round((speed - 22) / (110 - 22) * 255)    # Speed limitations [22 - 110mm/sec]
        self._3f_controller.output_registers.r_fra = round((force - 15) / (60 - 15) * 255)     # Force limitations [15 - 60N]

        # Call the service asynchronously
        future1 = self._3f_controller_cli.call_async(self._3f_controller)

        # Rviz gripper 
        self._gripper_req.width = float(width)   
        self._gripper_req.gripper_name = "3f"
        future2 = self._gripper_client.call_async(self._gripper_req)

        # Wait for the result
        response1 = self.wait_future(future1, timeout=15)
        response2 = self.wait_future(future2, timeout=15)

        return response1

    #@tool
    def manipulate_left_gripper(self, width: int=85, speed: int=110, force: int=20) -> Robotiq2F85GripperCommand.Response:   # Defaults to open gripper with fast speed and minimum force
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
            self.get_logger().error('Requested right gripper width exceeds gripper capabilities')
            return 'Requested gripper width exceeds gripper capabilities'
        if speed < 20 or speed > 150:
            self.get_logger().error('Requested right gripper speed exceeds gripper capabilities')
            return 'Requested right gripper speed exceeds gripper capabilities'
        if force < 20 or force > 235:
            self.get_logger().error('Requested right gripper force exceeds gripper capabilities')
            return 'Requested right gripper force exceeds gripper capabilities'

        self._2f_req.width = float(width)   # Opening in millimeters. Must be between 0 and 85 mm.
        self._2f_req.speed = float(speed)   # Speed in mm/s. Must be between 20 and 150 mm/s.
        self._2f_req.force = float(force)   # Force in N. Must be between 20 and 235 N.

        # Publish command to left gripper
        future1 = self._2f_client.call_async(self._2f_req)

        # Rviz gripper
        self._gripper_req.width = float(width)   # Opening in millimeters. Must be between 0 and 85 mm.
        self._gripper_req.gripper_name = "2f"
        future2 = self._gripper_client.call_async(self._gripper_req)

        # Wait for the result
        response1 = self.wait_future(future1, timeout=15)
        response2 = self.wait_future(future2, timeout=15)

        return response1
    
    #@tool
    def get_current_pose(self, arm: str) -> GetCurrentPose.Response:
        """
        Retrieves the current pose of the specified robot arm.

        Args:
            arm (str): The robot arm to query. Must be either 'left' or 'right'.

        Returns:
            dict: A dictionary containing the current pose of the arm with the
                  following structure:
                  {
                          'x': float,
                          'y': float,
                          'z': float
                          'roll': float,
                          'pitch': float,
                          'yaw': float
                  If the service call fails, returns a string indicating the failure.
        """
        self.get_logger().info(f"Received request to get current pose for {arm} arm")
        self.robot_pose_req.arm = arm

        future = self.robot_pose_client.call_async(self.robot_pose_req)

        # Wait for the result
        response = self.wait_future(future, timeout=15)

        if response is None:
            self.get_logger().error('Service call failed')
            return "Service call failed"

        if response.success:
            self.get_logger().info(f"Current pose for {arm} arm retrieved successfully")

            # Convert quat to euler
            rpy = self.quat_to_euler([response.pose.orientation.w, response.pose.orientation.x, response.pose.orientation.y, response.pose.orientation.z])

            # Add offsets to the pose to match the world coordinates
            pose_dict = {
            'position': {
                'x': response.pose.position.x + 0.02903434,
                'y': response.pose.position.y + 0.03177714,
                'z': response.pose.position.z - 0.84
            },
            'orientation': {
                'roll': rpy[0] + 180,   #Not sure why 180 this is needed...
                'pitch': rpy[1],
                'yaw': rpy[2] + 180     #Not sure why 180 this is needed...
            }
            }

            return pose_dict
        else:
            self.get_logger().error(f"Failed to get current pose for {arm} arm: {response.log}") 

        return response

    ################################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODELS -------------------------- #
    ################################################################################################

    def gui_handle_service(self, request, response):
        prompt = request.prompt  # prompt is a string

        # TEst image retrieval
        # self.request_rvis_image()

        # Convert to langgraph message
        query = HumanMessage(prompt)

        print("Received request")

        #If the user wants to clear the history, do so
        if "clear history" in prompt:
            os.system('clear')
            response.message = "History cleared."

            # Log the conversation
            self.save_snapshot()

            # Update config
            current_id = int(self.config["configurable"]["thread_id"])
            new_id = current_id + 1
            self.config["configurable"]["thread_id"] = str(new_id)

            # Append the initial prompt to the message state
            self.agent.update_state(self.config, {"messages": self.initial_prompt})

            return response
        
        # Run the graph
        # We stream the message through the agent (consider using this for updating GUI continuously)
        for event in self.agent.stream({"messages": [query]}, self.config, stream_mode="values"):
            event["messages"][-1].pretty_print()

        # Retrieve the last message from the agent and send it back to the user
        response.message = self.agent.get_state(self.config).values["messages"][-1].content

        return response       


def main(args=None):
    rclpy.init()
    node = LLMNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        node.get_logger().info('Beginning client, shut down with CTRL-C')
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt, shutting down.\n')
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()