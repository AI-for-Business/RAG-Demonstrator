import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore
from langchain.schema.document import Document
from llama_provider import get_embedding_function
from langchain_chroma import Chroma # type: ignore



# Define paths for the Chroma database and data directory
CHROMA_PATH = "chroma"
DATA_PATH = "data"

def updateDatabase(should_reset_db=False):
    if should_reset_db:
        clear_database()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    # Initialize a PDF directory loader to load all PDFs from DATA_PATH ("data" folder as stated above)
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    # Initialize a text splitter to break documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,               # Target maximum size (in characters) of each chunk
        chunk_overlap=80,             # Number of characters to overlap between chunks
        length_function=len,          # Function to measure the length of text
        is_separator_regex=False,     # Indicates if the separator is a regex pattern
    )
    # Split the documents into chunks
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    # Load the existing Chroma database or create a new one if it doesn't exist
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate unique IDs for each chunk based on source, page, and index
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Retrieve existing document IDs from the database to avoid duplicates
    existing_items = db.get(include=[])  # IDs are included by default
    existing_ids = set(existing_items["ids"])

    # Identify new chunks that are not already in the database
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    # Add new chunks to the database if any
    if len(new_chunks):
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)

def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")  # Source file path
        page = chunk.metadata.get("page")      # Page number
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            # Reset the chunk index when moving to a new page
            current_chunk_index = 0

        # Calculate the chunk ID
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Store the ID in the chunk's metadata
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    # Remove the Chroma database directory to reset the database
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    updateDatabase()
