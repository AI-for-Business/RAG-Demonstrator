import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

from get_embedding_function import get_embedding_function

# Define the path to the Chroma database directory
CHROMA_PATH = "chroma"

# Template for the prompt to be sent to the language model
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create a command-line interface to accept the query text as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Execute the retrieval-augmented generation (RAG) query
    query_rag(query_text)


def query_rag(query_text: str, model):
    # Prepare the Chroma database with the embedding function
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the database for similar documents, returning top 5 results with scores
    results = db.similarity_search_with_score(query_text, k=5)
    # Concatenate the contents of the retrieved documents to form the context
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # Create the prompt by filling in the template with context and the question
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)  # Uncomment this line to debug the generated prompt

    if model == 'Llama3.2':
        model = OllamaLLM(model="llama3.2")
        response_text = model.invoke(prompt)
    else:
        response_text = query_openai_model(prompt, model)

    # Extract source IDs from the retrieved documents for reference
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    
    # Format and print the response along with the sources used
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

def query_openai_model(prompt: ChatPromptTemplate, model: str):
    load_dotenv()
    api_key = os.getenv("OPENAI_KEY")

    if not api_key:
        raise ValueError("No key found in .env file")
    
    os.environ["OPENAI_API_KEY"] = api_key
    
    llm = OpenAI(model=model)

    return llm.invoke(prompt)

if __name__ == "__main__":
    main()
