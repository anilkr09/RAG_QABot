import pdfplumber
from docx import Document
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embeddings import ChromaEmbeddingFunction
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv(override=True)

# Check if API key is available
cohere_api_key = os.getenv('COHERE_API_KEY')
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is not set")

class DocumentProcessor:
    def __init__(self):
        logging.info("Initializing DocumentProcessor")
        try:
            # Initialize ChromaDB
            logging.info("Initializing ChromaDB client")
            self.chroma_client = chromadb.PersistentClient(path="db")
            logging.info("ChromaDB client initialized successfully")
            
            # Create or get collection
            logging.info("Creating/getting ChromaDB collection")
            self.collection = self.chroma_client.get_or_create_collection(
                name="documents",
                embedding_function=ChromaEmbeddingFunction(cohere_api_key=cohere_api_key)
            )
            logging.info("ChromaDB collection initialized successfully")
            
            # Initialize text splitter
            logging.info("Initializing text splitter")
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            logging.info("Text splitter initialized successfully")
        except Exception as e:
            logging.error(f"Error in DocumentProcessor initialization: {str(e)}")
            raise

    def process_document(self, file):
        """Process uploaded document and store in ChromaDB"""
        logging.info(f"Processing document: {file.name}")
        try:
            # Extract text based on file type
            logging.info("Extracting text from document")
            text = self._extract_text(file)
            logging.info(f"Text extracted successfully, length: {len(text)}")
            
            # Split text into chunks
            logging.info("Splitting text into chunks")
            chunks = self.text_splitter.split_text(text)
            logging.info(f"Text split into {len(chunks)} chunks")
            
            # Generate metadata
            logging.info("Generating metadata for chunks")
            metadatas = [{"source": file.name, "chunk_index": i} for i in range(len(chunks))]
            logging.info("Metadata generated successfully")
            
            # Add to ChromaDB
            logging.info("Adding chunks to ChromaDB collection")
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=[f"{file.name}_chunk_{i}" for i in range(len(chunks))]
            )
            logging.info("Chunks added to collection successfully")
        except Exception as e:
            logging.error(f"Error processing document: {str(e)}")
            raise

    def _extract_text(self, file):
        """Extract text from different file formats"""
        logging.info(f"Extracting text from file: {file.name}")
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(file)
        elif file_extension == '.docx':
            return self._extract_from_docx(file)
        elif file_extension == '.txt':
            return file.read().decode('utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _extract_from_pdf(self, file):
        """Extract text from PDF files"""
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, file):
        """Extract text from DOCX files"""
        doc = Document(file)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
