from langchain_google_genai import ChatGoogleGenerativeAI
from mainTools import tools
from dotenv import load_dotenv
from langchain import hub

load_dotenv()

CONFIGURATIONS={
    'temperature':0.7,
    'model':"gemini-1.5-flash",
}
llm=ChatGoogleGenerativeAI(model=CONFIGURATIONS['model'], temperature=CONFIGURATIONS['temperature'])

system_prompt = hub.pull("caller").messages[0].content

def caller_node(state):
    messages = [
        {"role": "system", "content": system_prompt},
    ]+state['messages']
    model_with_tools=llm.bind_tools(tools,tool_choice='any')
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


    
