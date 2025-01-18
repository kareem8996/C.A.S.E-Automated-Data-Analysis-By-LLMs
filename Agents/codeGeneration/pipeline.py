"""
pipeline.py

This module sets up a state graph for the application, defining the nodes and edges for the workflow.
It integrates various components such as the caller,coder, planner, tools, and designer to create a complete pipeline.

Dependencies:
- typing_extensions
- operator
- langgraph.graph
- caller
- planner
- mainTools
- designer
- langchain_core.messages
- coder
- os
- sys
- Database

Usage:
1. Ensure that the required dependencies are installed.
2. Set up the necessary environment variables in a .env file.
3. Use the generate_visualizations function to generate visualizations based on the project ID.

Classes:
- State: A TypedDict class to represent the state of the application.

Functions:
- generate_visualizations: Generates visualizations based on the project ID.

Variables:
- builder: An instance of StateGraph to build the state graph.
- graph: The compiled state graph.
"""

from typing_extensions import TypedDict,Annotated,NotRequired
import operator
from langgraph.graph import StateGraph, START, END
from caller import caller_node
from planner import planner_node,planner_brancher,tool_brancher
from mainTools import tool_node
from designer import designer_chain
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage
from coder import coder_node
import operator
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Database import mainDatabase

class State(TypedDict):
    """
    A class to represent the state of the application.
    """
    project_id:str
    messages: Annotated[list[AnyMessage], operator.add]
    call: NotRequired[str]
    code_output: NotRequired[str]
    visualization: NotRequired[dict]
    next: NotRequired[str]



builder = StateGraph(State)
builder.add_node("planner", planner_node)
builder.add_node("caller", caller_node)
builder.add_node("tools", tool_node)
builder.add_node("coder", coder_node)

builder.add_edge(START, "planner")
builder.add_conditional_edges("planner", planner_brancher)
builder.add_edge('caller','tools')
builder.add_conditional_edges('tools',tool_brancher)
builder.add_edge('coder',END)
graph = builder.compile()

def generate_visualizations(project_id):
    data_report=mainDatabase.fetch_data_report(project_id)
    response=designer_chain.invoke({'data_report':data_report})
    print(response)
    visualizations=[]
    print(len(response.response))
    for design in response.response:
        response=graph.invoke({'project_id':project_id,'messages':[{"role":"human","content":str(design)}]})
        visualizations.append(response['visualization'])
    return visualizations      

visualizations=generate_visualizations(1)
