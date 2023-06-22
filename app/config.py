import logging
from functools import lru_cache

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    vector_db: str = "deeplake"
    vector_url: str = "hub://devmaxime/langchain-code"
    llm_model_name: str = "gpt-3.5-turbo"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()

settings = get_settings()

__all__ = ["settings"]