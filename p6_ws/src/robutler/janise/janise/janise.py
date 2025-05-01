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

# Internal modules
from utils.graph_states import ToolExecutionState

# Langgraph / Langchain libraries
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.tools.base import StructuredTool
from langsmith import traceable

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, RemoveMessage

from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from langchain.prompts import PromptTemplate


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
            PromptJanice, 'send_prompt', self.main_handle_service, callback_group=gui_service_cb_group
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
        self.sim_cam_client = self.create_client(GetSimCameraData, 'get_simulated_camera_data')
        self.sim_cam_req = GetSimCameraData.Request()

        self.bridge = CvBridge()
        self.color_img = None
        self.use_sim = False

        # Robot service client
        self.robot_plan_client = self.create_client(PlanMoveCommand, 'plan_move_command', callback_group=client_cb_group)
        self.robot_plan_req = PlanMoveCommand.Request()

        self.robot_execute_client = self.create_client(ExecuteMoveCommand, 'execute_move_command', callback_group=client_cb_group)
        self.robot_execute_req = ExecuteMoveCommand.Request()

        self.robot_pose_client = self.create_client(GetCurrentPose, 'get_pose', callback_group=client_cb_group)
        self.robot_pose_req = GetCurrentPose.Request()

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Get current time and date from OS and format it for log file differentiation
        self.current_time = os.popen('date +"%Y-%m-%d_%H-%M-%S"').read().strip()
        self.get_logger().info(f"Current time and date: {self.current_time}")

        self.object_file = 'src/robutler/object_detector/object_detector/lego_bricks_config.json'
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

        # The path to the tool calls JSON file
        self.tool_calls_path = 'src/robutler/janise/resource/tool_calls_test.json'
        self.user_prompt = None

        self.lego_bricks = {}

        with open(self.object_file, 'r') as file:
            self.lego_bricks = json.load(file)

        # Define the locations in the environment
        self.coordinates = { # Predefined poses for different locations
            'HOME_RIGHT_ARM': {'x': '0.1', 'y': '0.3', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'},
            'HOME_LEFT_ARM': {'x': '0.9', 'y': '0.3', 'z': "0.3", 'roll': '0', 'pitch': '0', 'yaw': '0'},
            'TAKE_IMAGE': {'x': '0.43', 'y': '0.73', 'z': '0.43', 'roll': '-83', 'pitch': '48', 'yaw': '-180'},
        }

        # Define the tools available to the LLM
        self.tools = [StructuredTool.from_function(self.get_predefined_locations_and_poses), 
                      StructuredTool.from_function(self.find_object), 
                      StructuredTool.from_function(self.manipulate_right_gripper), 
                      StructuredTool.from_function(self.manipulate_left_gripper), 
                      StructuredTool.from_function(self.move_to_pose),
                      StructuredTool.from_function(self.pick_up_object)]
        
        self.task_detector_tools = [StructuredTool.from_function(self.detected_failure), 
                                   StructuredTool.from_function(self.detected_success)]
                
        self.tool_node = ToolNode(self.tools)
        self.task_detector_tool_node = ToolNode(self.task_detector_tools)

        # load the project id and key from json file
        with open('src/robutler/janise/API_KEY.json') as f:
            api_data = json.load(f)
        API_KEY = api_data['API_KEY']

        # Set API key
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = API_KEY 

        # Initialise the model
        # Change this to the model you want to use. We might implement more
        self.model = ChatOpenAI(model="gpt-4.1-mini")

        # ------------------------- Isaac Sim Workflow ------------------------- #
        self.bound_model = self.model.bind_tools(self.tools)
        self.judge_model = self.model.bind_tools(self.task_detector_tools)
        self.think_model = self.model.bind_tools(self.tools, tool_choice='none') # Forced to not call any tools

        self.sim_memory = MemorySaver()

        # Define a new graph
        # Using graphs allows us to define the flow of the conversation
        # To grasp this, it might be helpful to read a bit about graph theory
        # For each node action taken, we can will store the state of the conversation i.e. the messages
        self.sim_workflow = StateGraph(MessagesState)

        # Define the two nodes we will cycle between
        # The action node is the node that can actually call the tool using langgraphs's ToolNode class
        # We could for an example also add an observation node for our evaluating model
        self.sim_workflow.add_node("Janise", self.model_Janise)
        self.sim_workflow.add_node("action", self.tool_node)
        self.sim_workflow.add_node("action2", self.task_detector_tool_node)
        self.sim_workflow.add_node("action3", self.task_detector_tool_node)
        self.sim_workflow.add_node("Socrates", self.model_Socrates)
        self.sim_workflow.add_node("sim_judge", self.model_sim_judge)
        self.sim_workflow.add_node("sim_subtask_judge", self.model_sim_subtask_judge)
        self.sim_workflow.add_node("sim_error_explainer", self.model_sim_error_explainer)
        self.sim_workflow.add_node("clear_history", self.clear_history)
        self.sim_workflow.add_node("sim_subtask_judge_task_success", self.sim_subtask_judge_task_success)

        # Set the entrypoint as `Janise`
        # This means that this node is the first one called
        #self.sim_workflow.add_edge(START, "Janise")
        #self.sim_workflow.add_edge("Janise",END)

        self.sim_workflow.add_edge(START, "Socrates")
        self.sim_workflow.add_edge("Socrates", "Janise")

        # We now add a conditional edge
        # This means that the edge taken is determined by the function passed in
        self.sim_workflow.add_conditional_edges(
            # First, we define the start node. We use `Janise`.
            # This means these are the edges taken after the `Janise` node is called.
            "Janise",
            # Next, we pass in the function that will determine which node is called next.
            self.sim_should_continue,
            # Next, we pass in the path map - all the possible nodes this edge could go to
            ["action", "sim_judge"],
        )

        # ---- Right side of chart, this is called if janise did not make a tool call ----
        self.sim_workflow.add_conditional_edges(        
            "sim_judge",
            # The function that will determine which node is called next.
            self.sim_judge_task_success,
            # Path map - all the possible nodes this edge could go to
            ["action2", END],
        )
        self.sim_workflow.add_edge("action2","sim_error_explainer")  # The judge made a tool call, we need activate the call before proceeding, even though we do not need the result, then proceed to the explainer.
        self.sim_workflow.add_edge("sim_error_explainer", "clear_history")
        self.sim_workflow.add_edge("clear_history", "Socrates")

        # ---- Left side of chart, this is called if janise made a tool call ----
        self.sim_workflow.add_edge("action", "sim_subtask_judge")
        self.sim_workflow.add_edge("sim_subtask_judge", "sim_subtask_judge_task_success")
        self.sim_workflow.add_edge("sim_subtask_judge_task_success", "Socrates")
        self.sim_workflow.add_edge("Socrates", "Janise")

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        self.sim_workflow_manager = self.sim_workflow.compile(checkpointer=self.sim_memory)


        # Comment in to save a png of the graph and show it
        """
        graph = self.sim_workflow_manager.get_graph()

        # Display the workflow graph using OpenCV
        graph_image_path = f"{self.conversation_log_folder}/workflow_graph_{self.current_time}.png"
        graph.draw_mermaid_png(
            draw_method=MermaidDrawMethod.PYPPETEER,
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
        self.sim_config = {"configurable": {"thread_id": "sim_1"}}

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
            - Safety is of utmost importance, so when in doubt always consult the user first. Especially for actions that move the robot.
                  
        """)

        self.initial_prompt = [
            self.initial_prompt_Janise,
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
        
        self.initial_prompt_Socrates = SystemMessage(content = """Your name is Socrates. You act as a critical thinker and must help the other LLM agent Janise to take proper action based on a user's request. 
                                                                You are to provide short and precise reasoning and guidance to Janise to ensure that the correct actions are taken. Your message is appended to the conversation for Janise to consider.
                                                                As Janise is controlling a dual arm robot you must provide her with insights to the physical world, while considering the robot's capabilities and limitations.
                                                                You are NOT allowed to call any tools yourself and can therefore only make suggestions for Janise to consider. You should always provide reasoning for your suggestions.
                                                                You are set to make suggestions to Janise after an incoming user request or after a tool call has returned.
                                                                You are never answering directly to the user, but only to Janise. Therefore, never take "you" in the user's request as if the user is talking to you. Janise is the only model communicating with the user.
                                                 
                                                                To help you reason better you are given an image of the workspace. This you can use to provide better guidance to Janise.

                                                                Also apply your guidance in the context of the user request. You are to ensure that the overarching goal is not forgotten.
                                                                """)
        
        self.initial_prompt_sim_judge = SystemMessage(content = """You are a task success judge. You will be provided an image and you are to determine if the given task is completed or not. If the task is completed, call the function "detected_success". If the task is not completed call the function "detected_failure".""")
        
        #self.initial_prompt_sim_error_explainer = SystemMessage(content = """You are a task error explainer. The task was not completed correctly and you must explain why. Provide a brief explanation of the error and how it can be avoided in the future. 
        #                                                        Aditonally you MUST asses if the task is even possible by calling a function EVERY TIME. If it is not possible to complete the task in the given scene, call the function "detected_failure". If there was a mistake in the aporach to solving the task, and it can be completed with the given options, call the function "detected_success". 
        #                                                        The following messages are the conversation history, and you can use this to provide a better explanation of the error:""")

        self.initial_prompt_sim_error_explainer = SystemMessage(content = """You are a task error explainer. The task was not completed correctly and you must explain why. Provide a brief explanation of the error and how it can be avoided in the future.  
                                                                The following messages are the conversation history, and you can use this to provide a better explanation of the error:""")
        
        self.initial_prompt_sim_subtask_judge = SystemMessage(content = """You are a task success judge. You will be provided an image and you are to determine if the given tool calls are completed or not. If the task is completed, call the function "detected_success". If the task is not completed call the function "detected_failure".""")

        # Append the initial prompt to the message statejudge_model
        self.sim_workflow_manager.update_state(self.sim_config, {"messages": self.initial_prompt})

        
        # ------------------------- real Workflow ------------------------- #

        # Variable to help format dictionary
        self.function_call_id = 1

        # Define model nodes
        self.task_detector_model = self.model.bind_tools(self.task_detector_tools)
        self.correction_model = self.model.bind_tools(self.tools)
        self.plan_tool_call_model = self.model.bind_tools(self.tools)

        self.real_workflow = StateGraph(ToolExecutionState)
        self.real_config = {"configurable": {"thread_id": "real_1"}}
        self.real_memory = MemorySaver()

        self.real_workflow.add_node("init_real", self.init_real_execution)
        self.real_workflow.add_node("plan_tool_call", self.plan_tool_call)
        self.real_workflow.add_node("execute_tool", self.tool_node)  
        self.real_workflow.add_node("success_detector", self.call_success_detector)
        self.real_workflow.add_node("error_corrector", self.call_error_corrector)
        self.real_workflow.add_node("detector_action", self.task_detector_tool_node)
        self.real_workflow.add_node("corrector_action", self.tool_node)

        self.real_workflow.add_edge(START, "init_real")
        self.real_workflow.add_edge("init_real", "plan_tool_call")
        self.real_workflow.add_edge("plan_tool_call", "execute_tool")
        self.real_workflow.add_edge("execute_tool", "success_detector")

        self.real_workflow.add_edge("success_detector", "detector_action")

        self.real_workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "detector_action",
            # Next, we pass in the function that will determine which node is called next.
            self.check_successful_task,
            # Next, we pass in the path map - all the possible nodes this edge could go to
            ["error_corrector", "execute_tool", END],
        )

        #TODO: Add a condition to check if the task was successful
        self.real_workflow.add_edge("error_corrector", "corrector_action")
        self.real_workflow.add_edge("corrector_action", "success_detector")

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        self.real_workflow_manager = self.real_workflow.compile(checkpointer=self.real_memory)

        # Comment in to save a png of the graph and show it
        """
        graph = self.real_workflow_manager.get_graph()
        
        # Display the workflow graph using OpenCV
        graph_image_path = f"{self.conversation_log_folder}/workflow_graph_{self.current_time}.png"
        graph.draw_mermaid_png(
            draw_method=MermaidDrawMethod.PYPPETEER,
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

        self.initial_prompt_success_detector = SystemMessage(content = """ 
                                                                        You are a part of a robotic cell consisting of two collaborative KUKA iiwa 7 robots, each with 7 degrees of freedom (DoF).
                                                                        The setup includes a left and right side, each equipped with its respective robot arm.
                                                                        Given a task a fully featured pipeline of LLM and VLM agents are generating a list of tool calls required to solve the task.
                                                                        This pipeline is integrated in an Isaac Sim environment where the robot cell is simulated with all it components.
                                                                        A valid sequence of tool calls is generated by iteratively trying different sequences in the simulation.
                                                                        The sequence is then passed to the pipeline that runs the physical cell. This pipeline calls the tool one at a time in the provided order.

                                                                        As the given sequence has only been validated in simulation, it is possible that the sequence of tool calls is not valid in the real world.
                                                                        Therefore, your task is to determine whether the subtask or tool call was successful or not. 
                                                                        To determine this, you are given the called tool name and its returned results.
                                                                        If you consider the tool call / subtask to be successful, you should call the function "detected_success".
                                                                        Otherwise call the function "detected_failure". Notice, it is not enough for the tool to simply return a result to bes successful.
                                                                        You must read the results and determine whether the tool call was successful or not.
                                                             
                                                                        Always provide reasoning for your decision before calling the tool.
                                                             
                                                                        Based on your response the pipeline will either continue to the next subtask or correct the previous one by using another corrector agent.""")       

        self.initial_prompt_corrector = SystemMessage(content = """
                                                                You are a part of a robotic cell consisting of two collaborative KUKA iiwa 7 robots, each with 7 degrees of freedom (DoF).
                                                                The setup includes a left and right side, each equipped with its respective robot arm.
                                                                Given a task a fully featured pipeline of LLM and VLM agents are generating a list of tool calls required to solve the task.
                                                                This pipeline is integrated in an Isaac Sim environment where the robot cell is simulated with all it components.
                                                                A valid sequence of tool calls is generated by iteratively trying different sequences in the simulation.
                                                                The sequence is then passed to the pipeline that runs the physical cell. This pipeline calls the tool one at a time in the provided order.
                                                      
                                                                As the given sequence has only been validated in simulation, it is possible that the sequence of tool calls is not valid in the real world.
                                                                Therefore, another agent determines whether the subtask or tool call was successful or not. 

                                                                If the subtask was not successful, you are to provide a correction to the previous tool call.
                                                                You are given the called tool name and a failure description from the previous agent.
                                                                Given this information and the tool available to you, you are to provide a correction that completes the current subtask, so the next tool in the sequence can be called.
                                                      
                                                                A correction here refers to calling another tool or calling the same tool again with different parameters.
                                                                Notice you can not get any help or request any information from the other agent. Based on the chat history you must determine what the next step is.
                                                                Always call a tool.
                                                                """)

        # Append the initial prompt to the message state
        self.real_workflow_manager.update_state(self.real_config, {"messages": self.initial_prompt_success_detector})

        # Make the prompt template for the executor model
        # Define the prompt template
        self.plan_tool_call_prompt = PromptTemplate(
            input_variables=["current_function", "sim_tool_calls", "real_tool_calls"],
            template="""
                    You are a robot task corrector.

                    You are given:
                    - The planned function call and its arguments.
                    - The prior simulation outputs that were available when the function call was made.
                    - Fresh real-world observations.

                    Adjust the arguments for the real world, considering that small offsets or modifications may have been applied during planning.

                    Only adjust values if necessary.

                    The function to call is:
                    {current_function}

                    Simulated function calls and return values until now:
                    {sim_tool_calls}

                    Real-world function calls and return values until now:
                    {real_tool_calls}

                    You must call the same function as the current function but adjust the arguments to be valid in the real world.

                    Always provide reasoning for your decision before calling the tool.

                    Remember to format the tool calls appropriately.
                """
                
        )

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

    #######################################################################################
    # ------------------------------ LANGGRAPH FUNCTIONS -------------------------------- #
    #######################################################################################

    # If a tool is to be called, the action node is called otherwise the Janise node is called
    def sim_should_continue(self, state: MessagesState):
        """Return the next node to execute."""
        last_message = state["messages"][-1]
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "sim_judge"
        # Otherwise if there is, we continue
        return "action"
    
    def sim_judge_task_success(self, state: MessagesState):
        """Used by the judge to either end simulation task or continue"""

        tool = state["messages"][-1].tool_calls
        tool_name = tool[0]["name"]

        if tool_name == "detected_failure":
            return "action2" #We need to actiave the tool calls before proceeding
        elif tool_name == "detected_success":
            #TODO:SWITCH TO REAL SYSTEM
            return END # The system worked and we can move to the real system.
  
        # If it did not call anything we end anyways.
        return END
        
    def sim_error_task_sucess(self, state: MessagesState):
        """Used by the error explainer to either continue or end the task, beacuse it is not possible."""

        try: 
            tool = state["messages"][-1].tool_calls
            tool_name = tool[0]["name"]
            if tool_name == "detected_success":
                self.get_logger().info("Explainer asses that the task can be completed")
                return "action3" # The error explainer has determined that the task can be compeleted so we continue.
            elif tool_name == "detected_failure":
                self.get_logger().info("Detected failure")
                return END 
        except:
            self.get_logger().info("No tool was called by error explainer")

        # If they did not call anything we end anyways.
        return END
    
    def clear_history(self, state: MessagesState):
        """ Removes all but the initial prompts and the latest message from the message history. """
        self.get_logger().error("Clearing history")
        messages = state["messages"]
        return {"messages": [RemoveMessage(id=m.id) for m in messages[len(self.initial_prompt):-1]]}
    

    def sim_subtask_judge_task_success(self, state: MessagesState):
        """Used after the subtask judge to either remove or keep previous tool call"""
        messages = state["messages"]
        tool = state["messages"][-1].tool_calls
        tool_name = tool[0]["name"]

        if tool_name == "detected_failure":
            # Remove the latest two tool calls and go to socrates. 
            return "Socrates",{"messages": [RemoveMessage(id=messages[-1].id),RemoveMessage(id=messages[-2].id)]} 
        
        elif tool_name == "detected_success":
            return "Socrates" 
  
        # If it did not call anything we end anyways.
        self.get_logger().error("No tool was called by subtask judge")
        return END
    
    # If a tool is to be called, the action node is called otherwise the Janise node is called
    def successful_task(self, state: MessagesState):
        """Determines whether the error corrector should be called or not."""
        self.get_logger().info("Checking if task was successful")

        tool = state["messages"][-1]

        # Check if the model has called the "detected_failure" or "detected_success" function
        if tool.name == "detected_failure":
            self.get_logger().info("Detected failure")
            return "error_corrector"
        elif tool.name == "detected_success":
            self.get_logger().info("Detected success")
            return END
 
        # If no relevant function call, finish
        return END
    
    
    # If a tool is to be called, the action node is called otherwise the agent node is called
    @traceable
    def check_successful_task(self, state: ToolExecutionState):
        """Determines whether the error corrector should be called or not."""
        self.get_logger().info("Checking if task was successful")

        tool = state["messages"][-1]
        tools_available = state["tools_left"] # Check if there are any tools left

        # Check if the model has called the "detected_failure" or "detected_success" function
        if tool.name == "detected_failure":
            self.get_logger().info("Detected failure")
            return "error_corrector"
        elif tool.name == "detected_success":
            self.get_logger().info("Detected success")

            # Retrieve infromation about the executed tool
            executed_tool_AI = state["messages"][-4] # The AI message before the tool call
            executed_tool_message = state["messages"][-3] # The tool message

            function_name = executed_tool_AI.tool_calls[0].name
            function_args = executed_tool_AI.tool_calls[0].args
            function_returns = executed_tool_message.content

            self.get_logger().info(f"Executed tool: {function_name}")

            # Format the tool message to the desired structure
            tool_message = {
                    "function_name": function_name,
                    "args": function_args,
                    "return_values": function_returns
                }

            state["real_tools_results"][f"function_call_{self.function_call_id}"] = tool_message

            self.real_workflow_manager.update_state(self.cell_config, {"real_tool_calls": state["real_tools_results"]}) #Chack

            if tools_available:
                return "execute_tool"
            else: 
                return END
 
        # If no relevant function call, finish
        return END
    
    # This is a simple helper function to filter the messages
    # Modify this to fit your use case or use off-the-shelf tools from langchain_core
    def filter_messages(self, messages: list):
        # This is very simple helper function which only ever uses the last message
        return messages[-1:]
    
    @traceable
    def call_success_detector(self, state: ToolExecutionState):
        # We append the initial prompt to Janise
        state_shortened = {"messages": [self.initial_prompt_success_detector]}

        # Check if the last message is a HumanMessage or ToolMessage
        last_message = state["messages"][-1]
        
        if isinstance(last_message, HumanMessage):
            state_shortened["messages"].append(last_message)
        elif isinstance(last_message, ToolMessage):
            # A tool message must be preceeded by an AI message containg the tool call
            state_shortened["messages"].append(state["messages"][-2])
            state_shortened["messages"].append(last_message)

        response = self.task_detector_model.invoke(state_shortened["messages"])

        # We return a list, because this will get added to the existing list
        response.name = "Success_Detector"

        state["messages"].append(response)

        return state
    
    @traceable
    def call_error_corrector(self, state: ToolExecutionState):
        # We make the initial prompt to Janise
        state["messages"][0] = self.initial_prompt_corrector

        response = self.correction_model.invoke(state["messages"])

        # We return a list, because this will get added to the existing list
        response.name = "Error_Corrector"

        # Append the response to the message state
        state["messages"].append(response)

        return state
    
    
    # Define the function that calls the model
    # Takes in the cureent message history and returns the response
    def model_Janise(self, state: MessagesState):
        # We append the initial prompt to Janise
        state["messages"][0] = self.initial_prompt_Janise

        # Append the initial prompt to the message state
        self.sim_workflow_manager.update_state(self.sim_config, {"messages": state["messages"]})

        response = self.bound_model.invoke(state["messages"])
        # We return a list, because this will get added to the existing list
        response.name = "Janise"
        return {"messages": response}
    
    def model_Socrates(self, state: MessagesState):
        # We append an image to the CoT message
        #image_path = "image.jpg"

        # Resize the image to 524x524
        # Change this to get the actual image from the camera
        #original_image = cv2.imread(image_path)
        if self.use_sim:
            for i in range(5):
                request = GetSimCameraData.Request()
                future = self.sim_cam_client.call_async(request)

                # Wait for the result
                response = self.wait_future(future, timeout=10)

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
        state["messages"][0] = self.initial_prompt_Socrates
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
    
    
    def model_sim_judge(self, state_shortened: MessagesState):
        # This is the function that will be called to judge the simulation when janise determine the task is completed.
       
        resized_image_path = "/home/gustav/Dual_Kuka_LLM_Bachelor/p6_ws/src/robutler/janise/resource/resized_image.jpg"
       
        # Encode the resized image
        image = self.encode_image(resized_image_path)

        message = HumanMessage(
            content=[
                {"type": "text", "text": f"""The task was: "{self.user_prompt}". Here is an image of the workspace. 
                """},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}",},
                },
            ]
        )

        state_shortened = {"messages": [self.initial_prompt_sim_judge]}
        state_shortened["messages"].append(message)
        
        response = self.judge_model.invoke(state_shortened["messages"])
       
        response.name = "sim_judge"

        return {"messages": response}
    
    def model_sim_error_explainer(self, state: MessagesState):

        resized_image_path = "/home/gustav/Dual_Kuka_LLM_Bachelor/p6_ws/src/robutler/janise/resource/resized_image.jpg"
        
        # Encode the resized image
        image = self.encode_image(resized_image_path)

        message = HumanMessage(
            content=[
                {"type": "text", "text": f"""The task was: {self.user_prompt}. Here is an overview of the workspace.
                """},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}",},
                },
            ]
        )

        # We must replace the system message for Janise and Sokrates
        state["messages"][0] = self.initial_prompt_sim_error_explainer
        state["messages"].append(message)

        response = self.think_model.invoke(state["messages"])
        response.name = "sim_error_explainer"

        # METHOD 1 ---------------- POP (ONLY THE FIRST ONE WORKS)
        #self.get_logger().info(f"State before pop --------- {state['messages']}")
        state["messages"].pop() # Remove the image message
        #state["messages"].pop()
        #state["messages"].pop()
        #state["messages"].pop()
        #state["messages"].pop()
        #self.get_logger().info(f"State After 6 x pop --------- {state['messages']}")


        # Metod 2 ---------------- CLEAR AND ADD initial prompt (DOES NOT WORK)
        #state["messages"].clear 
        #state["messages"].append(self.initial_prompt_sim_error_explainer)
        #self.sim_workflow_manager.update_state(self.sim_config, {"messages": state["messages"]})


        # METHOD 3 ---------------- REMOVE ID (DOES NOT WORK)

        #messages = self.sim_workflow_manager.get_state(self.sim_config).values["messages"]
        #messages = state["messages"]
        #id=messages[-1].id
        #self.get_logger().info(f"---------id: {str(id)} ------------------")
        #for message in messages:
        #    if message.id == id:
        #        self.get_logger().info(f"Message with id {str(id)}: {str(message)}")
                #self.sim_workflow_manager.update_state(self.sim_config, {"messages": [RemoveMessage(id)]})
        #        break
        
        # IF I TRY TO DO IT TWICE I GET TOLD THE ID IS ALLREADY REMOVED
        #self.sim_workflow_manager.update_state(self.sim_config, {"messages": RemoveMessage(id)})
        #self.sim_workflow_manager.update_state(self.sim_config, {"messages": state["messages"]})
        

        # METHOD 4 ----------------- NEW THREAD (DOES NOT WORK)

        #current_id = self.sim_config["configurable"]["thread_id"]
        #new_id = current_id + "_another_run"
        #self.sim_config["configurable"]["thread_id"] = new_id
        #self.sim_workflow_manager.update_state(self.sim_config, {"messages": self.initial_prompt})
        
        # We 
        final = AIMessage(content=f"During previous atempts to solve the task, the following mistake(s) was detected: {response.text()}")

        # We return a list, because this will get added to the existing list
        return {"messages": final} 
    

    def model_sim_subtask_judge(self, state_shortened: MessagesState):
        # This is the function that will be called to judge each tool call made by janice.

        resized_image_path = "/home/gustav/Dual_Kuka_LLM_Bachelor/p6_ws/src/robutler/janise/resource/resized_image.jpg"
        image = self.encode_image(resized_image_path)

        self.get_logger().info(f"State subtask judge {state_shortened['messages']}")

        judge_tool_info = []

        for i in range(1, len(state_shortened["messages"])):
            if isinstance(state_shortened["messages"][-i], AIMessage):

                # The latest AI STATE WAS:
                self.get_logger().info(f"AI message {str(state_shortened['messages'][-i])}")

                self.get_logger().info(f"Number of tool calls is: {i-1}")
                self.get_logger().info(f"Tool message (right after): {str(state_shortened['messages'][-i+1])}")

                judge_tool_info.append(state_shortened["messages"][-i+1])
                judge_tool_info.append(". Which resulted in: ")


                self.get_logger().info(f"Tool result -2 after: {state_shortened['messages'][-i+2]}")
                                       
                #for j in range(1,i-1):
                #    self.get_logger().info("TOOL CALL RESULT FUND")
                #    self.get_logger().info(f"Tool result: {state_shortened['messages'][-i-j-1]}")

                #    judge_tool_info.append(state_shortened["messages"][-i-j-1])
                  
                break

        #for i, message in enumerate(reversed(state_shortened["messages"])):
        #    if isinstance(state_shortened["messages"][-i], AIMessage):
        #        self.get_logger().info(f"Number of tool calls is: {i-1}")
        #        self.get_logger().info(f"AI message {str(state_shortened['messages'][-i].tool_calls)}")

        #        judge_tool_info.append(state_shortened["messages"][-i].tool_calls)
        #        judge_tool_info.append(". Which resulted in: ")

        #        for j in range(i-1):
        #            self.get_logger().info(f"Tool call result {state_shortened['messages'][-i+j-1]}")

        #            judge_tool_info.append(state_shortened["messages"][-i+j-1])
                  
        #        break


        #self.get_logger().info(f"Judge tool info: {judge_tool_info}")
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": f"""The tools call(s) you must judge the success of are: {judge_tool_info}. Here is an image of the workspace which may be useful 
                """},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}",},
                },
            ]
        )

        state_shortened = {"messages": [self.initial_prompt_sim_subtask_judge]}
        state_shortened["messages"].append(message)
        
        response = self.judge_model.invoke(state_shortened["messages"])
       
        response.name = "sim_subtask_judge"

        return {"messages": response}
    
    @traceable
    def init_real_execution(self, state: ToolExecutionState):
        # Read the tool list from the tool_calls.json file
        tool_calls_path = 'src/robutler/janise/tool_calls.json'

        try:
            with open(tool_calls_path, 'r') as file:
                tool_calls = json.load(file)

            state["tool_list"] = tool_calls
            state["tools_left"] = tool_calls
            self.get_logger().info(f"Tool calls loaded from {tool_calls_path}")

        except FileNotFoundError:
            self.get_logger().error(f"File {tool_calls_path} not found.")
            return state
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Error decoding JSON from {tool_calls_path}: {e}")
            return state
        
        self.function_call_id = 1

        return state
    
    def update_real_tool_list(self, state: ToolExecutionState): #Chack
        

        return state
    
    @traceable
    def plan_tool_call(self, state: ToolExecutionState):
        # Get the tool call details from the state
        tool_call_key = list(state["tools_left"].keys())[0]
        current_tool_call = state["tools_left"][tool_call_key]

        # Extract all key-value pairs from the dictionary before the tool_call_key
        tool_call_dict = {k: v for k, v in state["tool_list"].items() if list(state["tool_list"].keys()).index(k) < list(state["tool_list"].keys()).index(tool_call_key)}

        # Convert the extracted dictionary to a string
        simulated_tool_calls = json.dumps(tool_call_dict, indent=4)

        if self.function_call_id > 1:
            real_tool_calls = json.dumps(state["real_tools_results"], indent=4)
        else:
            real_tool_calls = "None called yet"

        self.get_logger().info(f"Simulated tool calls: {simulated_tool_calls}")
        self.get_logger().info(f"Real tool calls: {real_tool_calls}")

        # Create a new message with the tool call details
        formatted_prompt = self.plan_tool_call_prompt.format(
                                                            current_function=current_tool_call,
                                                            sim_tool_calls=simulated_tool_calls,
                                                            real_tool_calls=real_tool_calls
                                                        )
        
        self.get_logger().info(f"Formatted prompt: {formatted_prompt}")

        message = SystemMessage(
            content=formatted_prompt
        )

        # Invoke the model with the tool call details
        response = self.plan_tool_call_model.invoke([message])

        # We return a list, because this will get added to the existing list
        response.name = "Plan_Tool_Call"

        # Append the response to the message state
        state["messages"].append(response)

        return state
    

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
        
        self.get_logger().info(f"\Requesting the Object detector service to find grasps for: {object_name}\n")

        # Call the object detection service, with the object name and the transformation matrix
        self.detector_req.object_name = object_name

        # Set the use_sim flag based on the current mode
        self.detector_req.use_sim = self.use_sim
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
                        'x': round(detected_obj.center_of_object.x,3),
                        'y': round(detected_obj.center_of_object.y,3),
                        'z': round(detected_obj.center_of_object.z,3)
                    },
                    'grasps': {}
                }

                for j, grasp in enumerate(detected_obj.grasps):
                    
                    ##### rotate the grasp 90 degrees around the z-axis of the grasp
                    T_90z = np.eye(4)
                    # Define the rotation matrix for -90 degrees around the z-axis
                    R_90z = Rotation.from_euler('z', -90, degrees=True).as_matrix()
                    T_90z[:3, :3] = R_90z

                    R_W_G = Rotation.from_euler('xyz', [grasp.orientation.x, grasp.orientation.y, grasp.orientation.z], degrees=True).as_matrix()
                    pose = np.array([grasp.position.x, grasp.position.y, grasp.position.z])
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
                    roll, pitch, yaw = [self.flip_if_near_180(a) for a in [roll, pitch, yaw]]

                    if pose[2] < 0 or grasp.grasp_width >= 0.1525:
                        self.get_logger().info(f'Grasp z value: {pose[2]}, grasp width: {grasp.grasp_width}')
                        continue

                    if j == 0:
                        grasp_name = 'Top down grasp'
                    else:
                        grasp_name = f'General grasp {j}'

                    self.objects_on_table[object_name]['grasps'][grasp_name] = {
                        'center': {
                            'x': round(pose_new[0],3),
                            'y': round(pose_new[1],3),
                            'z': round(pose_new[2],3)
                        },
                        'orientation': {
                            'roll': round(roll,3),
                            'pitch': round(pitch,3),
                            'yaw': round(yaw,3)
                        },
                        'width': 0 #round(grasp.grasp_width,3)
                    }
        print(f"\nThe object detection service returned the following objects: {self.objects_on_table}\n")

        return self.objects_on_table
    
    def flip_if_near_180(self, angle_deg):
        """
        If angle is near ±180, flip it to the equivalent small negative or positive.
        Assumes input is already in [-180, 180)
        """
        if angle_deg > 90:
            return angle_deg - 180
        elif angle_deg < -90:
            return angle_deg + 180
        return angle_deg
    
    #@tool
    def pick_up_object(self, pose: list, arm: str, object_width: int=0) -> bool:
        """
        Picks up an object by planning and executing a trajectory and closing the gripper.
        Args:
            pose (list): Target pose for the robot arm.
            arm (str): Specifies which arm to use ('left' or 'right').
            object_width (int, optional): Width of the object to grip in millimeters. Defaults to 0 mm.
        Returns:
            bool: True if the object was successfully picked up, False otherwise.
        """
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
            return False
        
        # Now plan the movement to the approach pose
        plan_response = self.plan_robot_trajectory(pose_approach, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan approach trajectory")
            return False
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute approach trajectory")
            return False
        
        # Now plan the movement to the pose
        plan_response = self.plan_robot_trajectory(pose, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return False
        
        # Execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return False
        
        # Close the gripper
        if arm == 'left':
            gripper_response = self.manipulate_left_gripper(width=object_width)
        else:
            gripper_response = self.manipulate_right_gripper(width=object_width)

        if gripper_response is None or not gripper_response.success:
            self.get_logger().error("Failed to close gripper")
            return False
        
        # At last lift the object to avoid collision when moving away
        plan_response = self.plan_robot_trajectory(pose_depart, arm)
        if plan_response is None or not plan_response.success:
            self.get_logger().error("Failed to plan grasp trajectory")
            return False
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute grasp trajectory")
            return False
        
        return True

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
            return False
        
        # The execute the planned trajectory
        execute_response = self.execute_planned_trajectory(arm)
        if execute_response is None or not execute_response.success:
            self.get_logger().error("Failed to execute trajectory")
            return False
        
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
    

    ################################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODELS -------------------------- #
    ################################################################################################

    def real_system(self, request, response):
        """Runs the tool list created by the Isaac Sim pipeline.
        LLMs or VLMs are only used to check if a subtask has been fulfilled
        and to correct potential failures.
        
        """
        # Check if the function call was successful and correct if necessary
        state = ToolExecutionState()
        #state["messages"] = [self.initial_prompt]
        for event in self.real_workflow_manager.stream(state, self.real_config, stream_mode="values"):
            event["messages"][-1].pretty_print()
        
        self.get_logger().info("Finished running from tool list")

        # If all tools have been called, we can return a success message
        response.message = "All tools have been called successfully."

        return response


    def sim_system(self,request, response):
        """ Generates the tool list uisng Isaac Sim """

        # Convert to langgraph message format
        query = HumanMessage(self.user_prompt)

        for event in self.sim_workflow_manager.stream({"messages": [query]}, self.sim_config, stream_mode="values"):
            event["messages"][-1].pretty_print()
            

        # ------------- Now the right tool calls have been generrated, so we save it to a json ------------- #

        # Retrieve the tool calls generated during the simulation workflow
        state_snapshot = self.sim_workflow_manager.get_state(self.sim_config).values
        messages = state_snapshot["messages"]
        
        # Go througt all the messages and find the tool calls 
        tool_list = {} 
        call_nr = 0
        for i, message in enumerate(messages):
            if isinstance(message, AIMessage) and message.tool_calls:
                for j, tool_call in enumerate(message.tool_calls):
                                    
                    # Find the result of the tool call(s)
                    if isinstance(messages[i + j + 1], ToolMessage):
                        tool_message = messages[i + j + 1]
                        
                    call_nr += 1
                    function_nr = f'function_call_{call_nr}'
                    tool_list[function_nr] ={
                        "function_name": tool_call["name"],
                        "args": tool_call["args"],
                        "return_values": json.dump(tool_message.content)
                    }                    
                
        # Write the tool calls to the JSON file
        try:
            with open(self.tool_calls_path, 'w') as file:
                json.dump(tool_list, file, indent=4)
                self.get_logger().info(f"Tool list written to {self.tool_calls_path}")

                response.message = "Tool list generated successfully."
        except Exception as e:
            self.get_logger().error(f"Failed to write tool list to {self.tool_calls_path}: {e}")
            response.message = "Tool list generation failed."

        return response

    def main_handle_service(self, request, response):
        self.get_logger().info("Request received")

        self.user_prompt = request.prompt  # prompt is a string

        #If the user wants to clear the history, do so
        if "clear history" in self.user_prompt:
            os.system('clear')
            response.message = "History cleared."

            # Log the conversation
            self.save_snapshot()

            # Update config
            current_id = int(self.sim_config["configurable"]["thread_id"])
            new_id = current_id + 1
            self.sim_config["configurable"]["thread_id"] = str(new_id)

            # Append the initial prompt to the message state
            self.sim_workflow_manager.update_state(self.sim_config, {"messages": self.initial_prompt})

            return response

        sim = True

        if sim:
            response = self.sim_system(request, response)
        else:
            response = self.real_system(request, response)

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