from typing import Any, Dict

from graph.state import GraphState
from graph.chains.retrieval import query_pinecone


def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Recover documents from the vectorstore based on the topic in the state.
    """
    print("---RETRIEVE---")
    question = state["question"]
    
    # Obtener el tema seleccionado si existe en el estado
    print(f"retrieve.py: Estado completo: {state}")
    
    # Forzar el uso de Pinecone si estamos en la sección de Renta
    if "topic" in state and state["topic"] == "Renta":
        print("FORZANDO USO DE PINECONE PARA RENTA")
        print(f"Pregunta: {question}")
        documents = query_pinecone(question)
        print(f"Recuperados {len(documents)} documentos de Pinecone")
        
        # Verificar las fuentes de los documentos
        for i, doc in enumerate(documents):
            source = doc.metadata.get('source', 'Desconocido')
            print(f"Documento {i+1}: {source}")
        
        return {"documents": documents}
    else:
        # Comportamiento normal para otros temas
        topic = state.get("topic", None)
        print(f"retrieve.py: Tema obtenido del estado: '{topic}', tipo: {type(topic)}")
        
        # Para otros temas o si no se especifica tema, usar Pinecone por defecto
        # Este es un cambio con respecto al original que usaba Chroma
        print("---USANDO PINECONE COMO FALLBACK---")
        documents = query_pinecone(question)
        print(f"---RECUPERADOS {len(documents)} DOCUMENTOS DE PINECONE---")
        
        # Verificar las fuentes de los documentos
        for i, doc in enumerate(documents):
            source = doc.metadata.get('source', 'Desconocido')
            print(f"Documento {i+1}: {source}")
    
        return {"documents": documents}
