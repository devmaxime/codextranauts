from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.tools import Tool
from langchain import OpenAI
import pinecone


from shared_code.config import settings


def search_pinecone_codebase(question):
    """
    Search in the Pinecone codebase for answers to your questions.

    Parameters:
        question (str): The question to ask.

    Returns:
        str: The answer to your question.
    """

    # Initialize Pinecone
    pinecone.init(
        api_key=settings.PINECONE_API_KEY,
        environment=settings.PINECONE_ENV,
    )

    # Define the index
    index_name = settings.PINECONE_INDEX_NAME
    index = pinecone.Index(index_name=index_name)

    # Define the vector store
    vectorstore = Pinecone(index, OpenAIEmbeddings().embed_query, "text")

    # Define the chain
    chain = load_qa_chain(OpenAI(temperature=0))

    number_of_relevant_documents = 5  # You can play with this value.

    docs = vectorstore.similarity_search(question, k=number_of_relevant_documents)

    return docs


def get_pinecone_codebase_tool():
    """
    Create a custom tool based on the search_pinecone_codebase function.

    Returns:
        Tool: The custom tool.
    """
    search_codebase_tool = Tool.from_function(
        func=search_pinecone_codebase,
        name="Search Codebase",
        description="Search the codebase for answers to your questions.",
    )

    return search_codebase_tool
