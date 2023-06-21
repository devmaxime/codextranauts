import os
import pinecone

from vectorizer import get_embedding_vector

# pinecone_key = os.getenv("PINECONE_KEY")
# pinecone_env = os.getenv("PINECONE_ENV")

INDEX_NAME = "indexvectornauts1"

# pinecone.init(
#     api_key=pinecone_key,
#     environment=pinecone_env  # find next to API key in console
# )

code_example = "def max(a,b): if a>b: return a else return b"


def main():
    # index = pinecone.Index(INDEX_NAME)

    vectors = get_embedding_vector(code_example)
    print(vectors)


if __name__ == '__main__':
    main()
