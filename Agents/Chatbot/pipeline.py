import operator
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, AnyMessage
from langgraph.graph import START, MessagesState, StateGraph
from typing_extensions import TypedDict,Annotated,NotRequired
from Chatbot import call_model
from dotenv import load_dotenv

load_dotenv()


builder = StateGraph(state_schema=MessagesState)

builder.add_edge(START, "model")
builder.add_node("model", call_model)

graph = builder.compile()
