import os
import pinecone as pc
from dotenv import load_dotenv
from utils.embeddings import get_query_embedding, get_docs_embeddings
import logging
from typing import List


class PineconeIndex:
    """A class that encapsulates interactions with a Pinecone index."""

    def __init__(self, index_name: str, dimension: int = 1536):
        """
        Initialize a Pinecone index.

        Parameters
        ----------
        index_name : str
            The name of the Pinecone index.
        dimension : int, optional
            The dimensionality of the index. Defaults to 1536.
        """
        load_dotenv()
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENV")
        if not all([api_key, environment]):
            raise ValueError(
                """Both PINECONE_API_KEY and PINECONE_ENV must be set in
                environment variables."""
            )
        pc.init(api_key=api_key, environment=environment)

        self.logger = logging.getLogger(__name__)
        self.index_name = index_name
        self.dimension = dimension
        self._index = None

    @property
    def index(self):
        """Get the Pinecone index, ensuring it exists."""
        if not self._index:
            self._ensure_index_exists()
        return self._index

    def _ensure_index_exists(self):
        """Ensures that the Pinecone index exists."""
        try:
            if self.index_name not in pc.list_indexes():
                pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                )
                self.logger.info(f"Index '{self.index_name}' created successfully.")

            self._index = pc.Index(index_name=self.index_name)
        except pc.errors.IndexAlreadyExistsError:
            self.logger.warning(f"Index '{self.index_name}' already exists.")
        except pc.errors.PineconeError as e:
            self.logger.error(
                f"Failed to ensure the index '{self.index_name}' exists: {e}"
            )
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def upsert_vectors(self, texts: List[str]):
        """
        Upserts a list of text strings to the Pinecone index.

        Parameters
        ----------
        texts : List[str]
            The list of text strings to upsert.

        Raises
        ------
        ValueError
            If 'texts' is not a non-empty list of strings.
        """

        # Validate inputs
        if not texts or not all(isinstance(text, str) for text in texts):
            raise ValueError("texts must be a non-empty list of strings.")

        try:
            vectors = [
                (str(i), get_docs_embeddings(text)[0], {"text": text})
                for i, text in enumerate(texts, start=1)
            ]
            self.index.upsert(vectors)
            self.logger.info(f"Upsert successful for {len(vectors)} vectors.")
        except pc.errors.UpsertError as e:
            self.logger.error(f"Upsert failed for vectors: {vectors}")
            self.logger.exception(e)
            raise
        except Exception as e:
            self.logger.error("Unexpected error occurred during upsert operation.")
            self.logger.exception(e)
            raise

    def query_index(self, query: str, k=3, filter=None):
        """
        Queries the Pinecone index.

        Parameters
        ----------
        query : str
            The query string.
        k : int, optional
            The number of results to return. Defaults to 3.
        filter : dict, optional
            The query filter.

        Raises
        ------
        ValueError
            If 'query' is not a non-empty string, 'k' is not a positive
            integer, or 'filter' is not a dictionary.
        """

        # Validate inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string.")
        if not isinstance(k, int) or k <= 0:
            raise ValueError("k must be a positive integer.")
        if filter is not None and not isinstance(filter, dict):
            raise ValueError("If provided, filter must be a dictionary.")
        filter = {} if filter is None else filter

        try:
            vector = get_query_embedding(query)
            result_vectors = self.index.query(
                vector=vector,
                include_metadata=True,
                top_k=k,
                filter=filter,
            )
            return result_vectors
        except pc.errors.QueryError as e:
            self.logger.error(f"Query failed for vector: {vector}")
            self.logger.exception(e)
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error: {str(e)} occurred during query operation."
            )
            self.logger.exception(e)
            raise


# index_name = os.getenv("PINECONE_INDEX_NAME")
# index = PineconeIndex(index_name=index_name)
