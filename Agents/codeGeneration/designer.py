from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

CONFIGURATIONS={
    'temperature':0.5,
    'model':"gemini-1.5-pro",
}
prompt = hub.pull("designer").messages[0].content

llm=ChatGoogleGenerativeAI(model=CONFIGURATIONS['model'], temperature=CONFIGURATIONS['temperature'])

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("user", "Here is the data report, based on it call the visualizations needed by following the system instruction:\n\n {data_report}"),
])

designer_chain=chain = prompt | llm | StrOutputParser()

