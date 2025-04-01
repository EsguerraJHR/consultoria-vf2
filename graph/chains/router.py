from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave API de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("No se encontró la clave API de OpenAI. Por favor, configúrela en las variables de entorno.")

class RouteQuery(BaseModel):
    destination: str = Field(description="The final topic the query is about")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=openai_api_key)
structured_llm_router = llm.with_structured_output(RouteQuery, method="function_calling")

system = """You are a routing assistant for a tax consultation firm.
    Given a query from the user, you should route it to the appropriate topic.
    If the query is about withholding taxes (retención en la fuente), route it to "retencion".
    If the query is not about a specific topic, if it's a greeting, or if you are unsure, route it to "general".
"""
router_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{query}"),
    ]
)

router = router_prompt | structured_llm_router
