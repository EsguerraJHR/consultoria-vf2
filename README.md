# Tributario Clean

Proyecto para el procesamiento de información tributaria utilizando LangGraph, Pinecone, y OpenAI.

## Estructura del Proyecto

- `graph/`: Contiene la implementación de LangGraph
  - `nodes/`: Nodos para el grafo
  - `chains/`: Cadenas de procesamiento para recuperar información
  - `topics/`: Temas tributarios
- `app.py`: Aplicación principal
- `requirements.txt`: Dependencias del proyecto con versiones exactas
- `setup.sh`: Script para configurar el entorno de desarrollo

## Requisitos Previos

- Python 3.9+
- Cuenta en OpenAI (para API key)
- Cuenta en Pinecone (para vectorización y búsqueda)

## Instalación y Entornos Virtuales

Este proyecto utiliza un entorno virtual específico (`venv_fixed`) con versiones exactas de las dependencias. Esto es crucial debido a cambios significativos en la API de Pinecone (de 2.x a 6.x) y actualizaciones en LangGraph.

### 1. Usando el script de configuración (Recomendado)

```bash
# Hacer ejecutable el script
chmod +x setup.sh

# Ejecutar el script
./setup.sh
```

Este script creará un entorno virtual llamado `venv_fixed` e instalará todas las dependencias necesarias con las versiones correctas.

### 2. Instalación manual

```bash
# Crear entorno virtual
python -m venv venv_fixed
source venv_fixed/bin/activate  # En Windows: venv_fixed\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
OPENAI_API_KEY=tu_api_key_de_openai
PINECONE_API_KEY=tu_api_key_de_pinecone
PINECONE_ENVIRONMENT=tu_region_de_pinecone  # Ejemplo: us-east-1
PINECONE_INDEX_NAME=tu_indice_de_pinecone   # Ejemplo: ejhr
```

## Ejecución en Entorno Local

### 1. Activar el entorno virtual

Siempre debes activar el entorno virtual `venv_fixed` antes de ejecutar cualquier comando:

```bash
source venv_fixed/bin/activate  # En Windows: venv_fixed\Scripts\activate
```

### 2. Ejecutar la aplicación principal

```bash
python app.py
```

### 3. Desarrollo con LangGraph Studio

Para depurar y visualizar el grafo:

```bash
langgraph dev
```

Esto iniciará un servidor local en `http://127.0.0.1:2024` y podrás acceder a la interfaz de LangGraph Studio en tu navegador usando la URL:

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

### 4. Pruebas de componentes individuales

Para probar la conexión con Pinecone:

```bash
python test_pinecone.py
```

## Despliegue en LangGraph Platform

LangGraph Platform permite desplegar tu aplicación directamente desde GitHub sin necesidad de infraestructura adicional.

### 1. Requisitos previos

- Una cuenta en [LangSmith](https://smith.langchain.com/)
- Tu código debe estar en un repositorio de GitHub (público o privado)

### 2. Configurar y Desplegar

#### Opción A: Usando la interfaz web

1. Inicia sesión en [LangSmith](https://smith.langchain.com/)
2. Selecciona "LangGraph Platform" en el menú lateral
3. Haz clic en "+ New Deployment" en la esquina superior derecha
4. Conecta tu cuenta de GitHub si es la primera vez
5. Selecciona este repositorio
6. Configura las variables de entorno necesarias:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_ENVIRONMENT`
   - `PINECONE_INDEX_NAME`
7. Haz clic en "Submit" para iniciar el despliegue

#### Opción B: Usando la CLI

1. Instala la CLI de LangGraph:
   ```bash
   pip install langgraph-cli
   ```

2. Inicia sesión en LangGraph Platform:
   ```bash
   langgraph auth login
   ```

3. Despliega la aplicación:
   ```bash
   langgraph app deploy
   ```

4. Sigue las instrucciones en la terminal para completar el despliegue

### 3. Usar la API desplegada

Una vez desplegada, puedes interactuar con tu aplicación a través de la API:

```python
from langgraph_sdk import get_client

# Reemplaza con la URL de tu despliegue
client = get_client(
    url="https://tu-despliegue.langgraphplat.com", 
    api_key="tu_langsmith_api_key"
)

# Ejecutar una consulta
result = client.runs.sync(
    None,  # Ejecución sin threads
    "agent",  # Nombre del asistente definido en langgraph.json
    input={
        "messages": [{
            "role": "human",
            "content": "¿Cuál es la tasa de retención en la fuente para honorarios?",
        }],
    },
)
print(result)
```

Para más detalles sobre el despliegue en LangGraph Platform, consulta la [documentación oficial](https://langchain-ai.github.io/langgraph/cloud/quick_start/).

## Notas sobre Versiones y Compatibilidad

Este proyecto requiere versiones específicas debido a cambios significativos en las APIs:

- **Pinecone**: Usamos la versión 6.0.2, que tiene una API completamente diferente a la 2.x
- **LangGraph**: Usamos la versión 0.3.18, compatible con la versión actual de LangGraph Platform
- **LangChain**: Usamos la versión 0.3.21 para garantizar compatibilidad con todos los componentes

Si experimentas problemas de compatibilidad, asegúrate de estar usando el entorno virtual `venv_fixed` y que todas las dependencias tengan las versiones exactas especificadas en `requirements.txt`.

## Solución de Problemas

### Conflictos de dependencias

Si encuentras errores de `ResolutionImpossible` durante el despliegue, verifica que todas las fuentes de configuración de dependencias (`requirements.txt`, `setup.py`, `pyproject.toml`) tengan versiones consistentes y exactas.

### Problemas con Pinecone

Si tienes problemas con la conexión a Pinecone, verifica:
1. Que tu API key sea correcta
2. Que el índice exista en tu cuenta
3. Que estés usando la región correcta
4. Que estés usando la API correcta para la versión 6.x de Pinecone

## Recursos Adicionales

- [Documentación de LangGraph](https://langchain-ai.github.io/langgraph/)
- [Documentación de Pinecone](https://docs.pinecone.io/docs/overview)
- [Despliegue en LangGraph Platform](https://langchain-ai.github.io/langgraph/cloud/quick_start/)

## Contribuir

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Haz push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request 

## Ejecución con Streamlit

Este proyecto también cuenta con una interfaz gráfica construida con Streamlit que permite interactuar con el asistente jurídico tributario de manera más amigable.

### Instalación de dependencias para Streamlit

```bash
# Activar el entorno virtual
source venv_fixed/bin/activate  # En Windows: venv_fixed\Scripts\activate

# Instalar dependencias específicas para Streamlit
pip install -r requirements-streamlit.txt
```

### Ejecutar la aplicación Streamlit

```bash
# Activar el entorno virtual
source venv_fixed/bin/activate  # En Windows: venv_fixed\Scripts\activate

# Iniciar la aplicación Streamlit
streamlit run Inicio.py
```

Esto abrirá la aplicación en tu navegador web, generalmente en la dirección `http://localhost:8501`.

### Estructura de la aplicación Streamlit

- `Inicio.py`: Página principal de la aplicación
- `pages/`: Contiene las subpáginas para cada tema tributario
  - `2_Renta.py`: Consultas sobre Impuesto de Renta
  - `3_Timbre.py`: Consultas sobre Impuesto de Timbre
  - `4_Retencion.py`: Consultas sobre Retención en la Fuente
  - `5_IVA.py`: Consultas sobre IVA
  - Otras páginas para temas adicionales

### Funcionalidades en la interfaz

- Consulta conversacional con el asistente
- Visualización de citas y referencias
- Acceso a los documentos fuente utilizados
- Seguimiento del flujo de procesamiento de cada consulta

### Despliegue en Streamlit Cloud

La aplicación puede ser desplegada en Streamlit Cloud:

1. Sube el código a un repositorio GitHub
2. Conéctate a [Streamlit Cloud](https://streamlit.io/cloud)
3. Selecciona tu repositorio
4. Configura las variables de entorno (las mismas que en el archivo `.env`)
5. Despliega la aplicación 