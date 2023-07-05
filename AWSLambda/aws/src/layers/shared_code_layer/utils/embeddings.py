import os
from typing import List, Optional
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging
import time

load_dotenv()

logger = logging.getLogger(__name__)


def initialize_embeddings():
    logging.basicConfig(level=logging.INFO)
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.critical("OPENAI_API_KEY not set in environment variables.")
            raise ValueError(
                "OPENAI_API_KEY not set in environment variables."
            )
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
        List of embeddings for each document in the input list or None if
        an error occurs.
    """
    try:
        return embeddings.embed_documents(docs)
    except Exception as e:
        logger.error("Failed to generate document embeddings: %s", e)
        return None


def get_docs_embeddings_in_batches(
    docs: List[str],
    batch_size=15,
) -> Optional[List[float]]:
    '''Todo'''
    batches = [docs[i:i + batch_size] for i in range(0, len(docs), batch_size)]

    combined_results = []
    for i, batch in enumerate(batches):
        # Process the batch and extend the combined results
        combined_results.extend(get_docs_embeddings(batch))

        # If this is not the last batch, then wait for 1 minute
        if i < len(batches) - 1:
            time.sleep(60)  # wait for 60 seconds

    return combined_results


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
