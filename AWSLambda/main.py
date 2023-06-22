import os
import pinecone as pc

from codeFetcher import fetch_script_text
from pineconeUtils import insert_vectors
from vectorizer import get_embedding_vector

pinecone_key = os.getenv("PINECONE_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

INDEX_NAME = "indexvectornauts1"

pc.init(
    api_key=pinecone_key,
    environment=pinecone_env
)

code_example = "def max(a,b): if a>b: return a else return b"
url_test = "https://raw.githubusercontent.com/devmaxime/codextranauts/AWSLambda/AWSLambda/vectorizer.py"


def main():
    index = pc.Index(INDEX_NAME)

    code_test_text = fetch_script_text(url_test)

    embedding_vector = get_embedding_vector(code_test_text)

    # Flatten the embedding tensor
    # embedding_flat = embedding_vector.view(-1, embedding_vector.size(-1))

    # Convert the embedding tensor to a NumPy array
    # embedding_np = embedding_flat.detach().numpy().tolist()

    vector_id = "A"

    insert_vectors(index, [vector_id], [embedding_vector])


if __name__ == '__main__':
    main()
