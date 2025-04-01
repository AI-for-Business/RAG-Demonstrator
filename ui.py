import string
import streamlit as st
from llama_provider import install_llama3dot2
from populate_database import updateDatabase
from query_data import query_rag 
import os

st.set_page_config(page_title="RAG Demonstrator", page_icon="🔍")

DATA_PATH = "data"

def main():
    initialize_llama()
    # Set page title and icon
    st.title("RAG Prototype")
    
    with st.sidebar:
        model = select_model()
        temperature = select_temperature()
        upload_documents()

    chat(model, temperature)


def select_model():
    return st.selectbox("Modellauswahl", ('gpt-4', 'gpt-4o', 'gpt-4o-mini', 'o1', 'o1-mini', 'Llama3.2'))

def select_temperature():
    return st.slider(label="Kreativitätsausmaß", min_value=0.0, max_value=1.0, value=0.5)

def upload_documents():
    st.header("Dokumente hochladen")

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = set()

    uploaded_files = st.file_uploader(
        "Wähle Dokumente",
        accept_multiple_files=True,
        type=["pdf", "txt"],
        help="PDF oder txt",
    ) or []  # Ensure uploaded_files is always a list

    new_files = [file for file in uploaded_files if file.name not in st.session_state.uploaded_files]

    if new_files:
        with st.spinner("Uploading new files..."):
            for file in new_files:
                path = os.path.join(DATA_PATH, file.name)
                with open(path, "wb") as writer:
                    writer.write(file.getbuffer())
                st.session_state.uploaded_files.add(file.name)  # Track uploaded files

            updateDatabase()  # Only update if new files were uploaded
            st.success("Neue Dateteien hochgeladen und Vektordatenbank aktualisiert")

def chat(model, temperature):
    # Initialize chat history if not already in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Accept a new prompt from the user
    prompt = st.chat_input("Stelle eine Frage, um augmentierte Informationen zu erhalten")

    # Process the new message if one was submitted
    if prompt:
        # Append the new user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Build a human-friendly string of the entire conversation (optional formatting)
        chat_history_str = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in st.session_state.messages
        )
        
        # Use the new prompt and the chat history in your query
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                # Assume query_rag accepts a chat_history parameter (update your function accordingly)
                response = query_rag(prompt, model, temperature, history=chat_history_str)
        
        # Append the assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat history (each message is shown with its role)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

@st.cache_resource
def initialize_llama():
    install_llama3dot2()

if __name__ == "__main__":
    main()
