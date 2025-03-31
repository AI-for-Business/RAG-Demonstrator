import argparse
from langchain_chroma import Chroma # type: ignore
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_ollama import OllamaLLM # type: ignore
from dotenv import load_dotenv
import os

from llama_provider import get_embedding_function

# Define the path to the Chroma database directory
CHROMA_PATH = "chroma"

# Template for the prompt to be sent to the language model
PROMPT_TEMPLATE = """
You are an AI assistant using a Retrieval-Augmented Generation (RAG) system.

Here is the conversation history:

{history}

---

Now, answer the latest question using the following context:

{context}

---

Latest Question: {question}

Answer in the language in which the question is asked.

If you find relevant information in the context, quote it in your answer.

If you do not find any relevant information in the context, always indicate so in your answer and use your general knowledge to answer the question, if you feel like you know the answer. 
"""



def main():
    # Create a command-line interface to accept the query text as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Execute the retrieval-augmented generation (RAG) query
    query_rag(query_text, "Llama3.2", 0.5, "")


def query_rag(query_text: str, model: str, temperature: float, history: str =""):
    # Prepare the Chroma database with the embedding function
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the database for similar documents, returning top 5 results with scores
    results = db.similarity_search_with_score(query_text, k=5)
    # Concatenate the contents of the retrieved documents to form the context
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # Create the prompt by filling in the template with context and the question
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text, history=history)
    # print(prompt)  # Uncomment this line to debug the generated prompt

    if model == 'Llama3.2':
        ollama = OllamaLLM(model="llama3.2", temperature=temperature, base_url="http://ollama:11434")
        response_text = ollama.invoke(prompt)
    else:
        response_text = query_openai_model(prompt, model, temperature)

    # Extract source IDs from the retrieved documents for reference
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    
    # Format and print the response along with the sources used
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

def query_openai_model(prompt: str, model: str, temperature: float):
    load_dotenv()
    api_key = os.getenv("OPENAI_KEY")

    if not api_key:
        raise ValueError("No key found in .env file")
    
    os.environ["OPENAI_API_KEY"] = api_key
    
    llm = ChatOpenAI(model=model, temperature=temperature)

    # Call the chat model
    return llm.predict(prompt)

if __name__ == "__main__":
    main()
