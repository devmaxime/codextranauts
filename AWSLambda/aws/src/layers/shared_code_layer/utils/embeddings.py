import os
from typing import List, Optional
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


def initialize_embeddings():
    logging.basicConfig(level=logging.INFO)
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.critical("OPENAI_API_KEY not set in environment variables.")
            raise ValueError("OPENAI_API_KEY not set in environment variables.")
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        return embeddings
    except Exception as e:
        logger.critical("Failed to initialize OpenAIEmbeddings: %s", e)
        raise


embeddings = initialize_embeddings()


def get_docs_embeddings(docs: List[str]) -> Optional[List[float]]:
    """Generate embeddings for a list of documents using OpenAI Embeddings.

    Args:
        docs: List of documents as strings.

    Returns:
        List of embeddings for each document in the input list or None if an error occurs.
    """
    try:
        return embeddings.embed_documents(docs)
    except Exception as e:
        logger.error("Failed to generate document embeddings: %s", e)
        return None


def get_query_embedding(query: str) -> Optional[List[float]]:
    """Generate embedding for a query using OpenAI Embeddings.

    Args:
        query: The user query as a string.

    Returns:
        An embedding for the input query or None if an error occurs.
    """
    try:
        return embeddings.embed_query(query)
    except Exception as e:
        logger.error("Failed to generate query embedding: %s", e)
        return None
