import os
from pydantic import BaseSettings


# Note: don't forget to add environment variable to lambda


class Settings(BaseSettings):
    environment: str = "dev"
    vector_db: str = "pinecone"  # options: pinecone | deeplake
    llm_model_name: str = "gpt-3.5-turbo"
    template_name: str = "template_2"  # options: template_1 | template_2
    PINECONE_API_KEY: str = os.environ["PINECONE_API_KEY"]
    PINECONE_ENV: str = os.environ["PINECONE_API_KEY"]
    PINECONE_INDEX_NAME: str = os.environ["PINECONE_INDEX_NAME"]
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]


settings = Settings()
