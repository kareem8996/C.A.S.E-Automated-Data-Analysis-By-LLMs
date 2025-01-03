from typing_extensions import TypedDict,Annotated
import operator

class State(TypedDict):
    """
    A class to represent the state of the application.
    """
    input: str
    messages: Annotated[list,operator.add]











