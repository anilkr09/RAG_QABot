# Personal Document QA Bot

A chatbot that can answer questions about your personal documents using LangChain, ChromaDB, Cohere, and Streamlit.

## Features

- Upload and process multiple document types (PDF, DOCX, TXT)
- Interactive chat interface
- Semantic search using ChromaDB
- Powered by Cohere for accurate responses
- Clean and intuitive Streamlit UI
## Demo

<img width="1318" alt="image" src="https://github.com/user-attachments/assets/2b16bf75-9bd3-437d-8c8e-30cfb64e82b4" />




<img width="1318" alt="image" src="https://github.com/user-attachments/assets/d9ab3bb0-56b3-4bb1-9c1f-0bc5284e4fd1" />



-Uploaded document 

<img width="1019" alt="image" src="https://github.com/user-attachments/assets/bdb6e4c0-311f-4a6a-a67f-b9c6e4a1be10" />


## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Cohere API key:
   ```bash
   cp .env.example .env
   ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload your documents using the sidebar
2. Click "Process Documents" to index them
3. Ask questions about your documents in the chat interface
4. Get AI-powered responses based on your document content

## Technical Stack

- LangChain (>=0.1.0): For document processing and QA chain
- LangChain-Cohere (>=0.0.1): For Cohere integration
- ChromaDB (>=0.3.0): Vector store for document embeddings
- Cohere (>=4.37): For embeddings and chat completions
- Streamlit (>=1.22.0): Web interface
- Supporting libraries:
  - pdfplumber (>=0.9.0): PDF processing
  - python-docx (>=0.8.11): DOCX processing
  - python-dotenv (>=1.0.0): Environment management
