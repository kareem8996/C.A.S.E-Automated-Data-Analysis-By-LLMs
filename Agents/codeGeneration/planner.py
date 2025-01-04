from typing import Literal
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END
from langgraph.types import Command
from langchain_core.messages import  ToolMessage

from dotenv import load_dotenv
load_dotenv()

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: ['coder','caller']. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
class Planner(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["coder", "caller"]



def planner_node(state) -> Command[Literal["coder", "caller"]]:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
    messages = [
        {"role": "system", "content": system_prompt},
    ]+state["messages"]
    response = llm.with_structured_output(Planner).invoke(messages)
    goto = response["next"]
    return Command(goto=goto)


def should_fallback(state) -> Literal["__end__", "caller"]:
    messages = state["messages"]
    failed_tool_messages = [msg for msg in messages if isinstance(msg, ToolMessage) and msg.additional_kwargs.get("error") is not None]
    if failed_tool_messages:
        return "caller"
    return END

