from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from mainTools import tool_node
CONFIGURATIONS={
    'temperature':0.7,
    'model':"gemini-1.5-pro",
}
llm=ChatGoogleGenerativeAI(model=CONFIGURATIONS['model'], temperature=CONFIGURATIONS['temperature'])

prompt=""
tools=[]

def coder_node(state):
    # WILL DO IT NEXT TIME
    return {'call':""}


    
