import streamlit as st
from query_data import query_rag 

def main():
    # Set page title and icon
    st.set_page_config(page_title="RAG Demonstrator", page_icon="🔍")
    
    # Title and description
    st.title("RAG Prototype")
    st.markdown("Enter your query to retrieve augmented information.")

    uploadDocuments()

    with st.form(key='query_form'):
        user_query = st.text_input(
            label="Enter your query:", 
            placeholder="Ask a question about your documents..."
        )
        submit_button = st.form_submit_button(label='Query')
    
    # Process query when submitted
    if submit_button and user_query:
        with st.spinner('Retrieving and generating response...'):
            try:
                response = query_rag(
                    query_text=user_query, 
                )
                
                # Display response
                st.subheader("Response")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


def uploadDocuments():
    with st.sidebar:
        st.header("Document Upload")

        # File uploader that allows multiple file uploads
        uploaded_files = st.file_uploader(
            "Choose documents",
            accept_multiple_files=True,
            type=["pdf", "txt"],
            help="You can upload PDF, or TXT files.",
        )

        for file in uploaded_files:
            pass

    

if __name__ == "__main__":
    main()