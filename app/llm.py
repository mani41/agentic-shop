import os

from langchain_ollama import ChatOllama

from app.tools.product_tools import search_products_tool


llm = ChatOllama(
    model=os.environ.get("OLLAMA_MODEL", "qwen3:4b"),
    base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=float(os.environ.get("OLLAMA_TEMPERATURE", os.environ.get("TEMPERATURE", 0.7)))
)

llm_with_tools = llm.bind_tools(
    [
        search_products_tool
    ]
)