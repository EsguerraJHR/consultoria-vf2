"""
Grafo específico para consultas sobre Aduanas.

Este grafo implementa un flujo de procesamiento optimizado para consultas
sobre temas aduaneros, utilizando reranking para mejorar 
la relevancia de los documentos recuperados.
"""

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from graph.state import GraphState
from graph.topics.aduanas.nodes import (
    retrieve_documents,
    generate_response,
    verify_response
)

# Cargar variables de entorno
load_dotenv()

# Nombres de nodos
RETRIEVE = "retrieve"
GENERATE = "generate"
VERIFY = "verify"

# Crear el grafo
workflow = StateGraph(GraphState)

# Agregar nodos
workflow.add_node(RETRIEVE, retrieve_documents)
workflow.add_node(GENERATE, generate_response)
workflow.add_node(VERIFY, verify_response)

# Definir punto de entrada
workflow.set_entry_point(RETRIEVE)

# Conectar los nodos
workflow.add_edge(RETRIEVE, GENERATE)
workflow.add_edge(GENERATE, VERIFY)

# Definir conexiones condicionales
workflow.add_conditional_edges(
    VERIFY,
    lambda state: state["verify_result"],
    {
        "useful": END,  # Si la respuesta es útil, finalizar
        "not_useful": GENERATE,  # Si no aborda la pregunta, regenerar
        "not_supported": GENERATE,  # Si tiene alucinaciones, regenerar
    }
)

# Compilar el grafo
app = workflow.compile()

# Función auxiliar para configurar depuración
def set_debug(debug_mode):
    import graph.topics.aduanas.nodes as nodes
    nodes.DEBUG = debug_mode

# Para pruebas locales
if __name__ == "__main__":
    print("Probando grafo de Aduanas")
    result = app.invoke({"question": "¿Cómo se determina el valor en aduana para la importación de mercancías?"})
    print(f"Respuesta: {result['generation'][:100]}...") 