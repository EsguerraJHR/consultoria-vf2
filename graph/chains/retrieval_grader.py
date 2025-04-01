from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave API de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("No se encontró la clave API de OpenAI. Por favor, configúrela en las variables de entorno.")

class GradeDocuments(BaseModel):
    binary_score: bool = Field(description="Documents are helpful for answering the query, 'yes' or 'no'")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=openai_api_key)
structured_llm_grader = llm.with_structured_output(GradeDocuments, method="function_calling")

system = """You are a grader assessing whether a set of documents are helpful for answering a question. \n 
     Give a binary score 'yes' or 'no'. 'Yes' means that the documents are helpful for answering the query."""
retrieval_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Query: \n\n {query} \n\n Documents: {documents}"),
    ]
)

retrieval_grader: RunnableSequence = retrieval_prompt | structured_llm_grader
