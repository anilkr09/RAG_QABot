from typing import List
import logging
from langchain_cohere import CohereEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChromaEmbeddingFunction:
    def __init__(self, cohere_api_key: str):
        logging.info("Initializing ChromaEmbeddingFunction")
        try:
            self.embeddings = CohereEmbeddings(
                cohere_api_key=cohere_api_key,
                model="embed-english-v3.0"
            )
            logging.info("CohereEmbeddings initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing CohereEmbeddings: {str(e)}")
            raise
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        logging.info(f"Generating embeddings for {len(input)} texts")
        try:
            embeddings = self.embeddings.embed_documents(input)
            logging.info(f"Successfully generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logging.error(f"Error generating embeddings: {str(e)}")
            raise
