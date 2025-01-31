import streamlit as st
from populate_database import updateDatabase
from query_data import query_rag 
import os

DATA_PATH = "data"

def main():
    # Set page title and icon
    st.set_page_config(page_title="RAG Demonstrator", page_icon="🔍")
    
    # Title and description
    st.title("RAG Prototype")

    with st.sidebar:
        model = selectModel()
        temperature = selectTemperature()
        uploadDocuments()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your query to retrieve augmented information."):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = st.write(query_rag(prompt, model, temperature))

        st.session_state.messages.append({"role": "assistant", "content": response})

def selectModel():
    return st.selectbox("Model Selection", ('gpt-4', 'gpt-4o', 'gpt-4o-mini', 'o1', 'o1-mini', 'Llama3.2'))

def selectTemperature():
    return st.slider(label="Model temperature", min_value=0.0, max_value=1.0, value=0.5)

def uploadDocuments():
    st.header("Document Upload")

    # File uploader that allows multiple file uploads
    uploaded_files = st.file_uploader(
        "Choose documents",
        accept_multiple_files=True,
        type=["pdf", "txt"],
        help="You can upload PDF or TXT files.",
    )

    if uploaded_files:
        with st.spinner("Uploading files..."):
            for file in uploaded_files:
                path = os.path.join(DATA_PATH, file.name)
                with open(path, "wb") as writer:
                    writer.write(file.getbuffer())

            updateDatabase()
            st.success("Files uploaded and database updated!")
    else:
        return   

if __name__ == "__main__":
    main()