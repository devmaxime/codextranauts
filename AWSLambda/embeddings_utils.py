import os
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Here two methods that use Open AI embeddings model to generate
# embeddings for documents (i.e. texts) and for user query


def get_docs_embeddings(docs):
    doc_result = embeddings.embed_documents(docs)
    return doc_result


def get_query_embedding(query):
    query_result = embeddings.embed_query(query)
    return query_result
