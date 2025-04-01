"""
Nodos específicos para el grafo de Cambiario.
"""

from typing import Dict, List, Any
from langchain_core.documents import Document

from graph.state import GraphState
from graph.chains.retrieval import query_cambiario
from graph.chains.reranking import retrieve_with_reranking
from graph.chains.openai_generation import generate_with_openai
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader

# Variable global para depuración
DEBUG = False

def debug_print(message):
    """Imprime mensajes de depuración si DEBUG es True."""
    if DEBUG:
        print(message)

def retrieve_documents(state: GraphState) -> Dict[str, Any]:
    """
    Recupera documentos específicos de Cambiario usando reranking.
    """
    debug_print("---CAMBIARIO: RETRIEVE DOCUMENTS---")
    question = state["question"]
    
    # Usar reranking para mejorar la relevancia de los documentos
    debug_print(f"Consultando para: {question}")
    documents = retrieve_with_reranking(question, query_cambiario, top_k=8)
    debug_print(f"Recuperados {len(documents)} documentos después de reranking")
    
    # Verificar las fuentes de los documentos
    for i, doc in enumerate(documents):
        source = doc.metadata.get('source', 'Desconocido')
        debug_print(f"Documento {i+1}: {source}")
    
    # Añadir el tema al estado
    return {
        "documents": documents,
        "topic": "Cambiario"
    }

def generate_response(state: GraphState) -> Dict[str, Any]:
    """
    Genera una respuesta basada en la consulta y los documentos recuperados.
    """
    debug_print("---CAMBIARIO: GENERATE RESPONSE---")
    question = state["question"]
    documents = state["documents"]
    
    try:
        # Generar respuesta con OpenAI
        openai_response = generate_with_openai(question, documents)
        
        # Extraer la respuesta y las citas
        generation = openai_response["text"]
        citations = openai_response.get("citations", [])
        
        debug_print(f"Respuesta generada con {len(citations)} citas")
        debug_print(f"Longitud de la respuesta: {len(generation)} caracteres")
        
        # Verificar si la respuesta tiene la estructura esperada
        has_structure = "REFERENCIA" in generation and "ANÁLISIS" in generation
        
        # Devolver un diccionario con la generación y las citas
        return {
            "generation": generation,
            "citations": citations,
            "has_structure": has_structure
        }
    except Exception as e:
        debug_print(f"---ERROR EN GENERACIÓN: {str(e)}---")
        return {"generation": f"Error al generar respuesta: {str(e)}"}

def verify_response(state: GraphState) -> Dict[str, str]:
    """
    Verifica que la respuesta esté fundamentada en los documentos y responda a la pregunta.
    """
    debug_print("---CAMBIARIO: VERIFY RESPONSE---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    # Verificar si hay alucinaciones
    hallucination_score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )
    
    if hallucination_score.binary_score:
        debug_print("---RESULTADO: LA RESPUESTA ESTÁ FUNDAMENTADA EN LOS DOCUMENTOS---")
        
        # Verificar si la respuesta aborda la pregunta
        answer_score = answer_grader.invoke(
            {"question": question, "generation": generation}
        )
        
        if answer_score.binary_score:
            debug_print("---RESULTADO: LA RESPUESTA ABORDA LA PREGUNTA---")
            return {"verify_result": "useful"}
        else:
            debug_print("---RESULTADO: LA RESPUESTA NO ABORDA LA PREGUNTA---")
            return {"verify_result": "not_useful"}
    else:
        debug_print("---RESULTADO: LA RESPUESTA NO ESTÁ FUNDAMENTADA EN LOS DOCUMENTOS---")
        return {"verify_result": "not_supported"} 