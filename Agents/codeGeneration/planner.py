"""
planner.py

This module sets up a language model to plan the next steps in the workflow based on the state messages.
The language model is configured to choose the next node in the workflow.

Dependencies:
- langchain_google_genai
- pydantic
- langgraph.graph
- langchain_core.messages
- langchain
- dotenv

Usage:
1. Ensure that the required dependencies are installed.
2. Set up the necessary environment variables in a .env file.
3. Use the planner_node function to determine the next step in the workflow based on the state messages.

Classes:
- Planner: A Pydantic model to structure the output of the language model.

Functions:
- load_dotenv: Loads environment variables from a .env file.
- planner_node: Determines the next step in the workflow based on the state messages.
- planner_brancher: Returns the next node in the workflow based on the state.
- tool_brancher: Returns the next node in the workflow based on the state.

Variables:
- system_prompt: The system prompt template pulled from the hub.
"""
from typing import Literal
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END
from langchain_core.messages import  ToolMessage
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

system_prompt = hub.pull("planner").messages[0].content
class Planner(BaseModel):
    next: Literal["coder", "caller"]



def planner_node(state):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(Planner).invoke(messages)
    goto = response.next
    return {'next':goto}

def planner_brancher(state)-> Literal["coder", "caller"]:
    return state['next']

def tool_brancher(state)-> Literal["caller", "__end__"]:
    return state['next']