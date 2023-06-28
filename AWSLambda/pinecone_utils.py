import os
import pinecone as pc
from embeddings_utils import get_query_embedding, get_docs_embeddings


pinecone_key = os.getenv("PINECONE_KEY")
pinecone_env = os.getenv("PINECONE_ENV")


index_name = "test-pinecone-index"  # "indexvectornauts1"
pc.init(api_key=pinecone_key, environment=pinecone_env)

index = pc.Index(index_name=index_name)


def create_index(index_name, dimension=1536):
    # check if exists and, if yes, delete the index
    # if index_name in pc.list_indexes():
    #     pc.delete_index(index_name)

    # check if doesn't exist and, if doesn't, create the index
    if index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
        )


def upsert_vectors(index, texts):
    # TODO: how to handle ids?
    # TODO: what metadata to include?
    vectors = []
    for i, text in enumerate(texts, start=1):
        vectors.append((str(i), get_docs_embeddings(text)[0], {"text": text}))

    index.upsert(vectors)


def query_index(index, query, k=3, filter={}):
    vector = get_query_embedding(query)

    result_vectors = index.query(
        vector=vector,
        # include_values=True,
        include_metadata=True,
        top_k=k,
        filter=filter,
    )
    return result_vectors
