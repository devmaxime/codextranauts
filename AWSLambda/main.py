import os
import pinecone as pc
from code_fetcher import fetch_script_text
from pinecone_utils import upsert_vectors

# from dotenv import load_dotenv

# from embeddings_utils import docs_embeddings, query_embedding
# from vectorizer import get_embedding_vector


# # Load environment variables from .env
# load_dotenv()

pinecone_key = os.getenv("PINECONE_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

INDEX_NAME = "test-pinecone-index"  # "indexvectornauts1"

pc.init(api_key=pinecone_key, environment=pinecone_env)

code_example = "def max(a,b): if a>b: return a else return b"
url_test = "https://raw.githubusercontent.com/devmaxime/codextranauts/AWSLambda/AWSLambda/vectorizer.py"


def main(url):
    index = pc.Index(INDEX_NAME)

    code_test_text = fetch_script_text(url)

    upsert_vectors(index=index, texts=[code_test_text])

    # embedding_vector = get_embedding_vector(code_test_text)

# if __name__ == "__main__":
#     main(url_test)
