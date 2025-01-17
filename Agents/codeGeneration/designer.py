from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from pydantic import BaseModel
from typing import List

from dotenv import load_dotenv
load_dotenv()

CONFIGURATIONS={
    'temperature':0.5,
    'model':"gemini-1.5-flash",
}

class Designer(BaseModel):
    response: List[str]

system_prompt = hub.pull("designer").messages[0].prompt.template

llm=ChatGoogleGenerativeAI(model=CONFIGURATIONS['model'], temperature=CONFIGURATIONS['temperature'])

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "Here is the data report, based on it write the visualizations needed by following the system instruction:\n\n {data_report}"),
])

designer_chain=chain = prompt | llm.with_structured_output(Designer)

