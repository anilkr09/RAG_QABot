import os
import chromadb
import logging
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv(override=True)

# Check if API key is available
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is not set")

class QAChain:
    def __init__(self):
        logging.info("Initializing QAChain")
        try:
            # Initialize embeddings
            logging.info("Initializing Cohere embeddings")
            self.embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key, model="embed-english-v3.0")
            logging.info("Cohere embeddings initialized successfully")
            
            # Initialize vector store
            logging.info("Initializing Chroma vector store")
            self.vectorstore = Chroma(
                collection_name="documents",
                embedding_function=self.embeddings,
                client=chromadb.PersistentClient(path="db")
            )
            logging.info("Vector store initialized successfully")
            
            # Initialize LLM
            logging.info("Initializing Cohere LLM")
            self.llm = ChatCohere(
                cohere_api_key=cohere_api_key,
                model="command",  # Using stable model instead of nightly
                temperature=0,
                request_timeout=30  # Adding timeout
            )
            logging.info("Cohere LLM initialized successfully")
            
            # Create retriever with search configuration
            logging.info("Creating retriever with search configuration")
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
            logging.info("Retriever created successfully")
            
            # Create QA chain
            logging.info("Creating QA chain")
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True  # This will help us see which documents were used
            )
            logging.info("QA chain created successfully")
        except Exception as e:
            logging.error(f"Error in QAChain initialization: {str(e)}")
            raise

    def get_response(self, query):
        """Get response for user query"""
        logging.info(f"Processing query: {query}")
        try:
            # First, get relevant documents
            logging.info("Searching for relevant documents")
            docs = self.retriever.get_relevant_documents(query)
            logging.info(f"Found {len(docs)} relevant documents")
            for i, doc in enumerate(docs):
                logging.info(f"Document {i+1} content: {doc.page_content[:200]}...")
            
            # Then generate response using the documents
            logging.info("Generating response using relevant documents")
            try:
                response = self.qa_chain.invoke({"query": query})
                logging.info("Successfully generated response")
            except Exception as e:
                logging.error(f"Error in Cohere chat completion: {str(e)}")
                return f"Error: The model is taking too long to respond. Please try again. Details: {str(e)}"
            
            # Extract result from response
            result = response["result"] if isinstance(response, dict) else response
            logging.info(f"Final response: {result}")
            return result
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logging.error(error_msg)
            return error_msg
