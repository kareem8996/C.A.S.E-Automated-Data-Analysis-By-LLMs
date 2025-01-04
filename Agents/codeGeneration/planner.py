from typing import Literal
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END
from langgraph.types import Command
from langchain_core.messages import  ToolMessage
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

system_prompt = hub.pull("planner").messages[0].content
class Planner(BaseModel):
    next: Literal["coder", "caller"]



def planner_node(state) -> Literal["coder", "caller"]:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(Planner).invoke(messages)
    goto = response.next
    return Command(goto=goto)


def should_fallback(state) -> Literal["__end__", "caller"]:
    messages = state["messages"]
    failed_tool_messages = [msg for msg in messages if isinstance(msg, ToolMessage) and msg.additional_kwargs.get("error") is not None]
    if failed_tool_messages:
        return "caller"
    return END



# Example state with messages
state = {
    "messages": [
        {"role": "human", "content": '{"plot_type": "Pie Chart", "values": ["survived"], "names": ["alive", "dead"], "title": "Survival Distribution", "color": ["green", "red"]}'}
    ]
}

# Invoke the planner_node function
next_worker = planner_node(state)
print(f"Next worker: {next_worker}")