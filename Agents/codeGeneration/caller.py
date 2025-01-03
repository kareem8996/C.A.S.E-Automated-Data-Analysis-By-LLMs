from langchain_google_genai import ChatGoogleGenerativeAI
from mainTools import tools
CONFIGURATIONS={
    'temperature':0.7,
    'model':"gemini-1.5-pro",
}
llm=ChatGoogleGenerativeAI(model=CONFIGURATIONS['model'], temperature=CONFIGURATIONS['temperature'])

prompt=""

def caller_node(state):
    messages = [
        {"role": "system", "content": prompt},
    ]+state['messages']
    model_with_tools=llm.bind_tools(tools)
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


    
