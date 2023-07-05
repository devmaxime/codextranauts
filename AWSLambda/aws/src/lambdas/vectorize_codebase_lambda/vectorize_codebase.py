import os
import logging
from utils.pinecone import PineconeIndex
from utils.codebase import get_all_files, fetch_code_text, parse_code_text
import time

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
    logger.info(f"Vectorizing repo: {user}/{repo}")
    if not index_name:
        logger.error("Environment variable 'PINECONE_INDEX_NAME' is not set.")
        return

    try:
        # Create the PineconeIndex object
        logger.info("Pinecone: establishing connection...")
        index = PineconeIndex(index_name)

        if index is None:
            logger.error(f"Failed to create PineconeIndex with the name: {index_name}")
            raise
        logger.info("Pinecone: conntected.")

        # Get all file from the codebase
        logger.info("GitHub: loading files.")
        files = get_all_files(user, repo)
        logger.info(f"GitHub: {len(files)} files loaded.")

        for file in files:
            # check if already in pinecone
            logger.info(f"GitHub: loading file: ${file['name']}-{0}")
            exists = len(index.query_index_by_id(file["url"]).matches)

            # process file
            if not exists:
                code_text = fetch_code_text(file["download_url"])

                if code_text is None:
                    logger.error(f"Failed to fetch file: {file['download_url']}")
                    continue

                # parse python files and chunk them
                imports_string, code_chunks = parse_code_text(code_text)

                for i, code_chunk in enumerate(code_chunks):
                    # upsert
                    index.upsert_single_vector(text=code_chunk, file=file)
                    logger.info(f"Pinecone: uploaded {file['name']}-{i}")

            time.sleep(2)

    except Exception as e:
        logger.error(
            f"An error occurred during processing the code from: \
            {user}/{repo} \n{str(e)}"
        )


vectorize_codebase("devmaxime", "codextranauts")
