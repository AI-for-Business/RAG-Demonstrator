from langchain_ollama import OllamaEmbeddings # type: ignore
import requests
import os

def get_embedding_function():
    # Initialize the embeddings using the 'nomic-embed-text' model
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://ollama:11434")
    # Return the embeddings instance for use in other parts of the application
    return embeddings

def install_llama3dot2():
    requests.post('http://ollama:11434/api/pull', json={'model': 'llama3.2'})
