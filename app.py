import streamlit as st
from document_processor import DocumentProcessor
from qa_chain import QAChain
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Initialize DocumentProcessor and QAChain
@st.cache_resource
def initialize_processors():
    doc_processor = DocumentProcessor()
    qa_chain = QAChain()
    return doc_processor, qa_chain

def main():
    st.title("Personal Document QA Bot")
    
    # Initialize processors
    doc_processor, qa_chain = initialize_processors()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # File upload section
    st.sidebar.header("Document Upload")
    uploaded_files = st.sidebar.file_uploader(
        "Upload your documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        with st.sidebar:
            if st.button("Process Documents"):
                with st.spinner("Processing documents..."):
                    for file in uploaded_files:
                        doc_processor.process_document(file)
                    st.success("Documents processed successfully!")

    # Chat interface
    st.header("Ask Questions About Your Documents")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        logging.info(f"Received user prompt: {prompt}")
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info("Added user message to chat history")
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            logging.info("Displayed user message")

        # Generate response
        with st.chat_message("assistant"):
            logging.info("Generating assistant response")
            with st.spinner("Thinking..."):
                try:
                    response = qa_chain.get_response(prompt)
                    logging.info("Successfully generated response")
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    logging.info("Added assistant response to chat history")
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    logging.error(error_msg)
                    st.error(error_msg)

if __name__ == "__main__":
    main()
