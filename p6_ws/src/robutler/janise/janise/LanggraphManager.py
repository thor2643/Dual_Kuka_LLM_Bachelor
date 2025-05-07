# Import 
import yaml
import json
import os
import cv2

# Internal modules
from utils.graph_states import ToolExecutionState
from janise.janise import LLMNode

# Langchain imports
from langchain.tools.base import StructuredTool
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langsmith import traceable
from langchain.prompts import PromptTemplate

# ROS2 libraries
import rclpy
from rclpy.executors import MultiThreadedExecutor


class LanggraphManager(LLMNode):
    def __init__(self):
        super().__init__()

        # Define the tools available to the LLM
        self.tools = [StructuredTool.from_function(self.get_predefined_locations_and_poses), 
                      StructuredTool.from_function(self.find_object), 
                      StructuredTool.from_function(self.manipulate_right_gripper), 
                      StructuredTool.from_function(self.manipulate_left_gripper), 
                      StructuredTool.from_function(self.move_to_pose),
                      StructuredTool.from_function(self.pick_up_object)]
        
        self.task_detector_tools = [StructuredTool.from_function(self.detected_failure), 
                                   StructuredTool.from_function(self.detected_success)]
        
        self.all_tools = self.tools + self.task_detector_tools
                
        self.tool_node = ToolNode(self.tools)
        self.task_detector_tool_node = ToolNode(self.task_detector_tools)

        # Load prompts from an external YAML file
        with open('src/robutler/janise/resource/prompts.yaml', 'r') as prompts_file:
            self.prompts = yaml.safe_load(prompts_file)

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

        # Initialise the simulation workflow
        self._init_sim_workflow()

        # Initialise the simulation workflow
        self._init_real_workflow()

        
    def _init_sim_workflow(self):
        self.bound_model = self.model.bind_tools(self.tools)
        self.judge_model = self.model.bind_tools(self.task_detector_tools, tool_choice="any")
        self.subtask_judge_model = self.model.bind_tools(self.all_tools,tool_choice="any")                                                       
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
        self.sim_workflow.add_edge("sim_subtask_judge", "action3")
        self.sim_workflow.add_edge("action3", "sim_subtask_judge_task_success")
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

        self.initial_prompt_Janise = SystemMessage(content = self.prompts["initial_prompt_janise"])

        self.initial_prompt = [
            self.initial_prompt_Janise]
        """
            HumanMessage(content = "To which poses can the robot arm be moved?"),
            AIMessage(content = "The robot arms can be moved to any positions within the workspace. However, there is a function available that provides predefined poses and locations. Janise should consider calling that.",
                    name = "Socrates"),
            AIMessage(content = "",
                    tool_calls = [{"name": "get_predefined_locations_and_poses", "args": {}, "id": "call_pTZTKZcHPTOPxDn3qnViIWWu"}],
                    name = "Janise"),
            ToolMessage(content = "{'HOME_RIGHT_ARM': {'x': '0.1', 'y': '0.3', 'z': '0.3', 'roll': '0', 'pitch': '0', 'yaw': '0'}, 'HOME_LEFT_ARM': {'x': '0.9', 'y': '0.3', 'z': '0.3', 'roll': '0', 'pitch': '0', 'yaw': '0'}, 'TAKE_IMAGE': {'x': '0.43', 'y': '0.73', 'z': '0.43', 'roll': '-83', 'pitch': '48', 'yaw': '-180'}",
                        tool_call_id = "call_pTZTKZcHPTOPxDn3qnViIWWu"),
            AIMessage(content = "The function returns valid predefined poses for the robot arms. As this was all that was requested, Janise should now return this information to the user.",
                        name = "Socrates"),
            AIMessage(content = The robot arms can be moved to several predefined poses. Here are some of the poses:

                    1. **Home Position for Right Arm**:
                    - Coordinates: (0.1, 0.3, 0.3)
                    - Orientation: roll 0\u00b0, pitch 0\u00b0, yaw 0\u00b0

                    2. **Home Position for Left Arm**:
                    - Coordinates: (0.9, 0.3, 0.3)
                    - Orientation: roll 0\u00b0, pitch 0\u00b0, yaw 0\u00b0

                    Should you desire to move one of the arms to one of these positions, feel free to let me know.,
                    name = "Janise"),
            HumanMessage(content = "Move the red cup to the left side of the table."),
            AIMessage(content = "I see a white table with a red cup on it. In order to move the red cup, its location must be known. Janise should consider calling the function \"find_object\" to get the location of the red cup.",
                    name = "Socrates"),
            AIMessage(content = "",
                    additional_kwargs={'tool_calls': [{'id': 'call_GYSTkPcmHtckTbWL6bfegcPS', 'function': {'arguments': '{"object_name":"cup"}', 'name': 'find_object'}, 'type': 'function'}], 'refusal': None},
                    name = "Janise"),
            ToolMessage(content={'cup 1': {'center_object': {'x': 0.616, 'y': 0.319, 'z': 0.045}, 'grasps': {}}}, 
                    name='find_object', id='8c73eb54-7f37-4f46-81d8-564123ee37b3', tool_call_id='call_GYSTkPcmHtckTbWL6bfegcPS'), 
            ]
        """
        

        
        self.initial_prompt_old = [
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
        
        self.initial_prompt_Socrates = SystemMessage(content = self.prompts["initial_prompt_Socrates"])
        
        self.initial_prompt_sim_judge = SystemMessage(content = self.prompts["initial_prompt_sim_judge"])
        
        #self.initial_prompt_sim_error_explainer = SystemMessage(content = """You are a task error explainer. The task was not completed correctly and you must explain why. Provide a brief explanation of the error and how it can be avoided in the future. 
        #                                                        Aditonally you MUST asses if the task is even possible by calling a function EVERY TIME. If it is not possible to complete the task in the given scene, call the function "detected_failure". If there was a mistake in the aporach to solving the task, and it can be completed with the given options, call the function "detected_success". 
        #                                                        The following messages are the conversation history, and you can use this to provide a better explanation of the error:""")

        self.initial_prompt_sim_error_explainer = SystemMessage(content = self.prompts["initial_prompt_sim_error_explainer"])
        
        self.initial_prompt_sim_subtask_judge = SystemMessage(content = self.prompts["initial_prompt_sim_subtask_judge"])

        # Append the initial prompt to the message statejudge_model
        self.sim_workflow_manager.update_state(self.sim_config, {"messages": self.initial_prompt})

        
    def _init_real_workflow(self):
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

        self.initial_prompt_success_detector = SystemMessage(content=self.prompts["initial_prompt_success_detector"])

        self.initial_prompt_corrector = SystemMessage(content = self.prompts["initial_prompt_corrector"])

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
        """ Removes all but: initial prompts, user query prompt, and the latest message by the error explainer. """
        self.get_logger().error("Clearing history")
        messages = state["messages"]
        return {"messages": [RemoveMessage(id=m.id) for m in messages[len(self.initial_prompt)+1:-1]]}

    def sim_subtask_judge_task_success(self, state: MessagesState):
        """Used after the subtask judge to ignore or save previous tool call"""
        #self.get_logger().info(f"The state is {state}")

        messages = state["messages"]
        tool = state["messages"][-2].tool_calls
        tool_name = tool[0]["name"]

        if tool_name == "detected_failure":
            human_message = HumanMessage(content="The prevoius tool call was rejected by the subtask judge, it was not successful, please correct it.")
            return {"messages": [human_message]} 
        
        elif tool_name == "detected_success":   
            # Find the second latest ai message (Made by janise)
            for i in range(3,len(messages)):
                if isinstance(messages[-i], AIMessage):
                    # The tool calls from janise.
                    tool_message = messages[-i].tool_calls 

                    # We add the tool calls to the list of tool calls
                    for j in range(len(tool_message)):
                        # The result of each tool call
                        tool_result = messages[-i+j+1].content

                        call_nr = len(self.sim_tool_list)+1

                        function_nr = f'function_call_{call_nr}'

                        self.sim_tool_list[function_nr] ={
                            "function_name": tool_message[j]["name"],
                            "args": tool_message[j]["args"],
                            "return_values": json.dumps(tool_result)
                        } 

                        #self.get_logger().info(f"Tool call {str(self.sim_tool_list)} added to the list of tool calls")
                    break

            human_message = HumanMessage(content="The tool call was accepted by the subtask judge")
            return {"messages": [human_message]}
  
        self.get_logger().error("Critical error. No tool was called by subtask judge")
        human_message = HumanMessage(content="Critical error. No tool was called by subtask judge")
        return {"messages": [human_message]}
    
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

            print(executed_tool_message)
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

            self.real_workflow_manager.update_state(self.real_config, {"real_tool_calls": state["real_tools_results"]})

            if tools_available:
                return "execute_tool"
            else: 
                return END
 
        # If no relevant function call, finish
        return END
    
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
        #self.get_logger().info(f"The state is {state}")  

        # Get image of cell (Either simulated or real)
        image = self.get_image()

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
        response = self.think_model.invoke(state["messages"])

        # Delete the image from history to save tokens
        state["messages"].pop()

        # Convert to Human message, such that Janise does not think she answered herself.
        #response_human = HumanMessage(content=response_2.text())
        response.name = "Socrates"

        # We return a list, because this will get added to the existing list
        return {"messages": response}
    
    
    def model_sim_judge(self, state_shortened: MessagesState):
        # This is the function that will be called to judge the simulation when janise determine the task is completed.
       
        # Get image of cell (Either simulated or real)
        image = self.get_image()
        
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

        # Get image of cell (Either simulated or real)
        image = self.get_image()

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

        state["messages"].pop() # Remove the image message
        
        response.content = f"During previous atempts to solve the task, the following mistake(s) was detected: {response.text()}"
        
        # We return a list, because this will get added to the existing list
        return {"messages": response} 

    def model_sim_subtask_judge(self, state_shortened: MessagesState):
        # This is the function that will be called to judge each tool call made by janise

        # Get image of cell (Either simulated or real)
        image = self.get_image()

        judge_tool_info = []

        # Loop through the messages in reverse order to find the last AI message (This is beacuse janise can make multiple tool calls)
        for i in range(1, len(state_shortened["messages"])):
            if isinstance(state_shortened["messages"][-i], AIMessage): 
                self.get_logger().info(f"Number of tool calls made by Janise: {i-1}")

                judge_tool_info.append(state_shortened["messages"][-i].tool_calls)
                judge_tool_info.append(". Which resulted in: ")

                # Add every tool call result to the tool_info list       
                for j in range(i-1):
                    judge_tool_info.append(state_shortened["messages"][-i+j+1])

                break
     
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
        
        response = self.subtask_judge_model.invoke(state_shortened["messages"])
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
        
        # Write the tool calls to the JSON file
        try:
            with open(self.tool_calls_path, 'w') as file:
                json.dump(self.sim_tool_list, file, indent=4)
                self.get_logger().info(f"Tool list written to {self.tool_calls_path}")

                response.message = "Tool list generated successfully."
        except Exception as e:
            self.get_logger().error(f"Failed to write tool list to {self.tool_calls_path}: {e}")
            response.message = "Tool list generation failed."

        return response

    ################################################################################################
    # -------------------------- INTERACTION WITH LARGE LANGUAGE MODELS -------------------------- #
    ################################################################################################

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

        sim = False

        if sim:
            response = self.sim_system(request, response)

            #Debbugging
            #returns = self.find_object("bottle")
            #response.message = "done"
        else:
            response = self.real_system(request, response)

        return response


def main(args=None):
    rclpy.init()
    node = LanggraphManager()

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
   
        