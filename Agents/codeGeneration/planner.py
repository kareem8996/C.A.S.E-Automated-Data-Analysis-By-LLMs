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