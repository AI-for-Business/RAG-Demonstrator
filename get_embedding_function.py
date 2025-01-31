#from langchain_community.embeddings.ollama import OllamaEmbeddings #deprecated
from langchain_ollama import OllamaEmbeddings # type: ignore

def get_embedding_function():
    # Initialize the embeddings using the 'nomic-embed-text' model
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    # Return the embeddings instance for use in other parts of the application
    return embeddings
