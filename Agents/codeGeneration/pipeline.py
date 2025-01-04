from typing_extensions import TypedDict,Annotated,NotRequired
import operator
from langgraph.graph import StateGraph, START, END
from caller import caller_node
from planner import planner_node,should_fallback
from mainTools import tool_node
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage
from coder import coder_node
import operator

class State(TypedDict):
    """
    A class to represent the state of the application.
    """
    call: NotRequired[str]
    code_output: NotRequired[str]
    messages: Annotated[list[AnyMessage], operator.add]





builder = StateGraph(State)
builder.add_node("planner", planner_node)
builder.add_node("caller", caller_node)
builder.add_node("tools", tool_node)
builder.add_node("coder", coder_node)

builder.add_edge(START, "planner")
builder.add_edge('caller','tools')
builder.add_conditional_edges("tools", should_fallback)
builder.add_edge('coder',END)
graph = builder.compile()


print(graph.invoke(
    {"messages": [("human", '{"plot_type": "Pie Chart", "values": ["survived"], "names": ["alive", "dead"], "title": "Survival Distribution", "color": ["green", "red"]}')]},
))