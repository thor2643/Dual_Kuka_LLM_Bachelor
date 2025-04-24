from typing import Dict, Any, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class ToolExecutionState(TypedDict):
    """
    Represents the state of a tool execution process, including messages, tools available,
    the result of the last tool execution, and an optional evaluation.

    Attributes:
        messages (list[AnyMessage]): A list of messages, annotated with additional metadata.
        tools_left (Dict[str, Any]): A dictionary of tools remaining for execution, where the key
            is the tool name and the value can be any type or a more structured schema.
        last_tool_result (Any, optional): The result of the last executed tool. Defaults to None.
        evaluation (str, optional): An optional evaluation of the success of the tool execution
            process, typically provided by an LLM. Defaults to an empty string.
    """
    messages: Annotated[list[AnyMessage], add_messages]
    tool_list: Dict[str, Any]  # or a more structured type if your tools follow a strict schema
    tools_left: Dict[str, Any]  # or a more structured type if your tools follow a strict schema
    last_tool_result: Any = None  # optionally store latest tool output
    evaluation: str = ""  # optionally store LLM's evaluation of success
