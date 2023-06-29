import os
import logging
from utils.pinecone import PineconeIndex
from utils.codebase import get_all_files, fetch_code_text

from dotenv import load_dotenv

load_dotenv()

# Create a logger
logger = logging.getLogger(__name__)


index_name = os.getenv("PINECONE_INDEX_NAME")


def vectorize_codebase(user: str, repo: str) -> None:
    """
    Fetch a codebase from the provided URL and upload it into Pinecone.

    Args:
        user (str): GitHub username who owns the repo
        repo (str): name of the GitHub repo
    """

    # Check if the required environment variable is available
    if not index_name:
        logger.error("Environment variable 'PINECONE_INDEX_NAME' is not set.")
        return

    try:
        # Create the PineconeIndex object
        index = PineconeIndex(index_name)
        if index is None:
            logger.error(
                f"Failed to create PineconeIndex with the name: {index_name}"
            )
            return

        # Get all file from the codebase
        files = get_all_files(user, repo)
        code_texts = []

        # Loop through all files in the code base, parse, vectorize, and
        # upload to Pinecone
        for file in files:
            # Fetch the codebase
            code_text = fetch_code_text(file['download_url'])

            if code_text is None:
                logger.error(f"Failed to fetch file: {file['download_url']}")
                return
            code_texts.append(code_text)

            # TODO: figure out chunking for later
            # imports_string, code_chunks = parse_code_text(code_text)

        index.upsert_vectors(texts=code_texts, metadata=files)
        logger.info(
            f"Uploaded code from {user}/{repo} repo into Pinecone \
            successfully."
        )
    except Exception as e:
        logger.error(
            f"An error occurred during processing the code from: \
            {user}/{repo} \n{str(e)}"
        )


vectorize_codebase("devmaxime", "codextranauts")
