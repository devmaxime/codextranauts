import os
import logging
from utils.pinecone import PineconeIndex
from utils.codebase import get_all_files, fetch_code_text
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
            logger.error(
                f"Failed to create PineconeIndex with the name: {index_name}"
            )
            raise
        logger.info("Pinecone: conntected.")

        # Get all file from the codebase
        logger.info("GitHub: loading files.")
        files = get_all_files(user, repo)
        logger.info(f"GitHub: {len(files)} files loaded.")

        for file in files:
            # check if already in pinecone
            logger.info(f"GitHub: loading file: ${file['name']}")
            exists = len(index.query_index_by_id(file['url']).matches)

            # process file
            if not exists:
                code_text = fetch_code_text(file['download_url'])

                if code_text is None:
                    logger.error(
                        f"Failed to fetch file: {file['download_url']}"
                    )
                    continue

                # upsert
                index.upsert_single_vector(text=code_text, file=file)
                logger.info(f"Pinecone: vector uploaded: {file['name']}")

            time.sleep(2)

        # # Loop through all files in the code base, parse, vectorize, and
        # # upload to Pinecone
        # logger.info("Codebase: loading text files...")
        # code_texts = []
        # for file in files:
        #     # Fetch the codebase
        #     code_text = fetch_code_text(file['download_url'])

        #     if code_text is None:
        #         logger.error(f"Failed to fetch file: {file['download_url']}")
        #         return
        #     code_texts.append(code_text)
        #     time.sleep(1)

        # logger.info("Codebase: text files loaded")
        # # TODO: figure out chunking for later
        # # imports_string, code_chunks = parse_code_text(code_text)

        # logger.info("Vectorstore: upsearing vectors...")
        # index.upsert_vectors(texts=code_texts, metadata=files)
        # logger.info(
        #     f"Uploaded code from {user}/{repo} repo into Pinecone \
        #     successfully."
        # )
    except Exception as e:
        logger.error(
            f"An error occurred during processing the code from: \
            {user}/{repo} \n{str(e)}"
        )


vectorize_codebase("devmaxime", "codextranauts")
