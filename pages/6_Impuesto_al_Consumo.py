import streamlit as st
from dotenv import load_dotenv
import os
import time
import re
# Importar el grafo completo en lugar de solo los componentes individuales
from graph.topics.ipoconsumo.graph import app as ipoconsumo_app
from graph.chains.retrieval import query_ipoconsumo
from graph.chains.openai_generation import generate_with_openai
# Importar el módulo de reranking
from graph.chains.reranking import retrieve_with_reranking

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Consultas sobre Impuesto al Consumo",
    page_icon="🛒",
    layout="wide"
)

# Título de la página
st.title("Consultas sobre Impuesto al Consumo")

# Descripción de la página
st.markdown("""
Esta sección le permite realizar consultas específicas sobre el Impuesto al Consumo en Colombia.
La base de conocimiento incluye conceptos de la Dian sobre impuesto al consumo desde 2017 hasta 2024. Contiene 423 conceptos de la Dian sobre impuesto al consumo.
""", unsafe_allow_html=True)

# Verificar si la colección existe
try:
    import pinecone
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    index_name = "ipoconsumo"  # Índice específico para impuesto al consumo
    
    if not pinecone_api_key:
        st.warning("No se ha configurado la API key de Pinecone. Por favor, configura la variable PINECONE_API_KEY en el archivo .env.")
    else:
        # Inicializar Pinecone
        pc = pinecone.Pinecone(api_key=pinecone_api_key)
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        # Si no existe el índice específico de impuesto al consumo, usar el índice general
        if index_name not in existing_indexes:
            index_name = os.environ.get("PINECONE_INDEX_NAME", "ejhr")
            st.info(f"Usando el índice general {index_name} para consultas de Impuesto al Consumo.")
        
        # Inicializar estado de sesión para Impuesto al Consumo
        if "ipoconsumo_messages" not in st.session_state:
            st.session_state.ipoconsumo_messages = []
        
        # Función para formatear el texto con citas numeradas
        def formatear_texto_con_citas(texto, citas):
            """
            Formatea el texto con citas numeradas en HTML.
            """
            if not citas:
                return texto
            
            # Reemplazar los corchetes de cita por etiquetas HTML para mejorar la visualización
            # Primero, crear un diccionario de citas para acceder rápidamente a la información de la página
            citas_dict = {}
            for i, cita in enumerate(citas):
                citas_dict[i+1] = cita
            
            # Función para reemplazar cada cita con su versión HTML que incluye la página
            def reemplazar_cita(match):
                num_cita = int(match.group(1))
                # Simplificar: siempre devolver solo el número de cita sin la página
                return f'<sup>[{num_cita}]</sup>'
            
            texto_formateado = re.sub(r'\[(\d+)\]', reemplazar_cita, texto)
            
            return texto_formateado
        
        # Mostrar mensajes anteriores
        for message in st.session_state.ipoconsumo_messages:
            with st.chat_message(message["role"]):
                # Si hay citas, formatear el texto con ellas
                if message["role"] == "assistant" and "citations" in message and message["citations"]:
                    formatted_content = formatear_texto_con_citas(message["content"], message["citations"])
                    st.markdown(formatted_content, unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])
                
                # Si hay documentos, mostrarlos
                if "documents" in message:
                    with st.expander("Ver fuentes utilizadas"):
                        for i, doc in enumerate(message["documents"]):
                            source = doc.metadata.get('source', f'Documento {i+1}')
                            page = doc.metadata.get('page', None)
                            page_info = f" (Pág. {page})" if page and page != 0 else ""
                            st.markdown(f"**Fuente {i+1}:** `{source}{page_info}`")
                            st.markdown(f"```\n{doc.page_content}\n```")
                
                # Si hay citas, mostrarlas
                if "citations" in message and message["citations"]:
                    with st.expander("Ver referencias"):
                        for i, citation in enumerate(message["citations"]):
                            st.markdown(f"**[{i+1}]** `{citation['document_title']}`")
                            st.markdown(f"*\"{citation['cited_text']}\"*")
                
                # Si hay un flujo, mostrarlo
                if "flow" in message:
                    with st.expander("Ver flujo de procesamiento"):
                        st.markdown(message["flow"])
        
        # Input para la consulta
        query = st.chat_input("Escribe tu consulta sobre Impuesto al Consumo...")
        
        # Procesar la consulta
        if query:
            # Agregar la consulta del usuario a los mensajes
            st.session_state.ipoconsumo_messages.append({
                "role": "user", 
                "content": query
            })
            
            # Mostrar la consulta en la interfaz
            with st.chat_message("user"):
                st.markdown(query)
            
            # Mostrar un spinner mientras se procesa la consulta
            with st.chat_message("assistant"):
                # Crear un placeholder para mostrar el flujo en tiempo real
                flow_placeholder = st.empty()
                
                # Usar una lista para almacenar los pasos del flujo (evita problemas con nonlocal)
                flow_steps = []
                
                # Función para actualizar el flujo
                def update_flow(step):
                    flow_steps.append(f"- {step}")
                    flow_text = ""
                    for s in flow_steps:
                        flow_text += s + "\n"
                    flow_placeholder.markdown(f"**Procesando:**\n{flow_text}")
                
                # Mostrar el flujo de procesamiento
                update_flow(f"🔄 Iniciando procesamiento de la consulta sobre Impuesto al Consumo...")
                time.sleep(0.5)
                
                update_flow("🧠 Analizando la consulta...")
                time.sleep(0.5)
                
                update_flow("🔍 Ejecutando flujo RAG avanzado...")
                time.sleep(1)
                
                # Consultar directamente a Pinecone para Impuesto al Consumo con reranking
                try:
                    # Consultar documentos específicos de Impuesto al Consumo con reranking
                    print("Impuesto_al_Consumo.py: Consultando directamente a Pinecone (índice ipoconsumo)")
                    # Usar la función de reranking para mejorar la relevancia de los documentos
                    update_flow("🔍 Recuperando documentos iniciales de Pinecone...")
                    time.sleep(0.5)
                    
                    documents = retrieve_with_reranking(query, query_ipoconsumo, top_k=8)
                    print(f"Impuesto_al_Consumo.py: Recuperados {len(documents)} documentos de Pinecone con reranking")
                    
                    # Verificar si se encontraron documentos
                    if not documents:
                        update_flow("❌ No se encontraron documentos relevantes en Pinecone")
                        response = "Lo siento, no encontré información relevante sobre tu consulta en la base de conocimiento de Impuesto al Consumo. Por favor, intenta reformular tu pregunta o consulta otra base de conocimiento."
                        final_flow = '\n'.join(flow_steps)
                        flow_placeholder.empty()
                        st.markdown(response)
                        citations = []
                        documents = []
                    else:
                        update_flow(f"📝 Encontrados {len(documents)} documentos relevantes")
                        time.sleep(0.5)
                        
                        update_flow("🔄 Aplicado reranking para mejorar la relevancia")
                        time.sleep(0.5)
                        
                        update_flow("✍️ Generando respuesta especializada en Impuesto al Consumo...")
                        time.sleep(0.5)
                        
                        # Generar respuesta con OpenAI
                        openai_response = generate_with_openai(query, documents)
                        response = openai_response["text"]
                        citations = openai_response.get("citations", [])
                        
                        update_flow("🔎 Verificando que no haya alucinaciones...")
                        time.sleep(0.5)
                        
                        update_flow("✅ Verificando que la respuesta aborde la consulta...")
                        time.sleep(0.5)
                        
                        if citations:
                            update_flow(f"📌 Añadiendo {len(citations)} citas a la respuesta...")
                            time.sleep(0.5)
                        
                        update_flow("✨ Respuesta sobre Impuesto al Consumo generada con éxito!")
                        
                        # Guardar el flujo para mostrarlo en el historial
                        final_flow = '\n'.join(flow_steps)
                        
                        # Limpiar el placeholder
                        flow_placeholder.empty()
                        
                        # Formatear la respuesta con citas si existen
                        if citations:
                            formatted_response = formatear_texto_con_citas(response, citations)
                            st.markdown(formatted_response, unsafe_allow_html=True)
                        else:
                            st.markdown(response)
                        
                        # Mostrar las citas si existen
                        if citations:
                            with st.expander("Ver referencias"):
                                for i, citation in enumerate(citations):
                                    st.markdown(f"**[{i+1}]** `{citation['document_title']}`")
                                    st.markdown(f"*\"{citation['cited_text']}\"*")
                        
                        # Mostrar las fuentes utilizadas
                        with st.expander("Ver fuentes utilizadas"):
                            for i, doc in enumerate(documents):
                                source = doc.metadata.get('source', f'Documento {i+1}')
                                page = doc.metadata.get('page', None)
                                page_info = f" (Pág. {page})" if page and page != 0 else ""
                                st.markdown(f"**Fuente {i+1}:** `{source}{page_info}`")
                                st.markdown(f"```\n{doc.page_content}\n```")
                        
                        # Mostrar el flujo de procesamiento
                        with st.expander("Ver flujo de procesamiento"):
                            st.markdown(final_flow)
                    
                except Exception as e:
                    update_flow(f"❌ Error al consultar documentos de Impuesto al Consumo o generar respuesta: {str(e)}")
                    response = f"Lo siento, ocurrió un error: {str(e)}"
                    final_flow = '\n'.join(flow_steps)
                    flow_placeholder.empty()
                    st.markdown(response)
                    citations = []
                    documents = []
            
            # Agregar la respuesta del asistente a los mensajes
            st.session_state.ipoconsumo_messages.append({
                "role": "assistant", 
                "content": response,
                "documents": documents if 'documents' in locals() else [],
                "flow": final_flow if 'final_flow' in locals() else '',
                "citations": citations if 'citations' in locals() else []
            })
except Exception as e:
    st.error(f"Error al conectar con Pinecone: {str(e)}")

# Información adicional en el sidebar
with st.sidebar:
    st.header("Sobre el Impuesto al Consumo")
    st.markdown("""
    El Impuesto al Consumo es un tributo que grava el consumo de bienes y servicios específicos en Colombia, complementando el sistema del IVA.
    
    **Aspectos clave:**
    - Aplicable a servicios de restaurantes, telefonía móvil y vehículos
    - Incluye ciertos bienes específicos como licores y cigarrillos
    - Se considera un impuesto monofásico, que se aplica una sola vez
    
    Consulta en esta sección todo lo relacionado con las tarifas, excepciones y procedimientos de este impuesto.
    """)
    
    st.divider()
    
    st.write("**Base de conocimiento**")
    st.write("• 423 conceptos especializados")
    st.write("• Documentación oficial de la DIAN")
    st.write("• Actualizado hasta 2024") 