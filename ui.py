import streamlit as st
from query_data import query_rag  # Assuming this is your existing RAG query function

def main():
    # Set page title and icon
    st.set_page_config(page_title="RAG Prototype", page_icon="🔍")
    
    # Title and description
    st.title("RAG Prototype")
    st.markdown("Enter your query to retrieve augmented information.")
    
    # Query input section
    with st.form(key='query_form'):
        # Text input for user query
        user_query = st.text_input(
            label="Enter your query:", 
            placeholder="Ask a question about your documents..."
        )
        # Submit button
        submit_button = st.form_submit_button(label='Query')
    
    # Process query when submitted
    if submit_button and user_query:
        with st.spinner('Retrieving and generating response...'):
            try:
                # Call the RAG query function
                response = query_rag(
                    query_text=user_query, 
                )
                
                # Display response
                st.subheader("Response")
                st.write(response)
                '''
                with st.expander("Retrieved Documents"):
                    st.json(response.get('retrieved_docs', {}))
                '''
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Sidebar for additional controls
    st.sidebar.header("RAG Settings")
    st.sidebar.markdown("""
    Configure your RAG query parameters:
    - Adjust the number of retrieved documents
    - Control LLM temperature
    """)

if __name__ == "__main__":
    main()