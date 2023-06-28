import os
import logging
from urllib.parse import urlparse
from utils.pinecone import PineconeIndex
from utils.codebase import fetch_script_text

from dotenv import load_dotenv

load_dotenv()

# Create a logger
logger = logging.getLogger(__name__)


index_name = os.getenv("PINECONE_INDEX_NAME")


def process_codebase(url: str) -> None:
    """
    Fetch a codebase from the provided URL and upload it into Pinecone.

    Args:
        url (str): URL of the codebase to fetch.
    """
    # Validate the URL
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        logger.error(f"Invalid URL: {url}")
        return

    # Check if the required environment variable is available
    if not index_name:
        logger.error("Environment variable 'PINECONE_INDEX_NAME' is not set.")
        return

    return

    try:
        # Fetch the codebase
        codebase_text = fetch_script_text(url)
        if codebase_text is None:
            logger.error(f"Failed to fetch the codebase from the URL: {url}")
            return

        # Create the PineconeIndex object
        index = PineconeIndex(index_name)
        if index is None:
            logger.error(f"Failed to create PineconeIndex with the name: {index_name}")
            return

        # Upload the codebase into Pinecone
        index.upsert_vectors(texts=[codebase_text])
        logger.info(
            f"Uploaded the codebase from the URL: {url} into Pinecone successfully."
        )
    except Exception as e:
        logger.error(
            f"An error occurred during processing the codebase from the URL: {url}\n{str(e)}"
        )


url_test = "https://raw.githubusercontent.com/devmaxime/codextranauts"  # noqa
process_codebase(url_test)
