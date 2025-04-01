from setuptools import setup, find_packages

setup(
    name="tributario-api",
    version="0.1.0",
    description="API de consultoría tributaria con LangGraph",
    author="Hernando Castro Arana",
    author_email="hcastro@esguerrajhr.com",
    packages=["graph"] + find_packages(exclude=["venv", "venv_fixed", "tributario_clean"]),
    include_package_data=True,
    install_requires=[
        "langchain==0.3.21",
        "langchain-core==0.3.46",
        "langchain-community==0.3.20",
        "langchain-openai==0.3.9",
        "langgraph==0.3.18",
        "langgraph-api==0.0.31",
        "langgraph-checkpoint==2.0.21",
        "langgraph-cli==0.1.77",
        "langgraph-prebuilt==0.1.3",
        "langgraph-sdk==0.1.58",
        "pinecone==6.0.2",
        "openai==1.67.0",
        "tiktoken==0.9.0",
        "python-dotenv==1.0.1",
        "anthropic==0.49.0",
    ],
) 