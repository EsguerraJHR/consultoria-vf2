#!/bin/bash
# Script para configurar el entorno del proyecto Tributario

echo "Configurando entorno para el proyecto Tributario..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv_fixed
source venv_fixed/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "Configuración completada con éxito!"
echo ""
echo "Para activar el entorno virtual, ejecuta:"
echo "  source venv_fixed/bin/activate"
echo ""
echo "Para ejecutar la aplicación, ejecuta:"
echo "  python app.py"
echo ""
echo "Para ejecutar el panel de desarrollo de LangGraph, ejecuta:"
echo "  langgraph dev"
echo ""
echo "Recuerda configurar las variables de entorno en un archivo .env:"
echo "  OPENAI_API_KEY=tu_api_key"
echo "  PINECONE_API_KEY=tu_api_key"
echo "  PINECONE_ENVIRONMENT=tu_region"
echo "  PINECONE_INDEX_NAME=tu_indice" 