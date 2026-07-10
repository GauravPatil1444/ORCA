# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Astra DB
    ASTRA_DB_APPLICATION_TOKEN: str
    ASTRA_DB_API_ENDPOINT: str
    
    # LLM & Agents
    GROQ_API_KEY: str
    
    # Langfuse Prompt Registry
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    
    # OWST Web Routing (Google Custom Search)
    GOOGLE_SEARCH_KEY: str
    GOOGLE_SEARCH_CX: str
    GOOGLE_SEARCH_URL: str = "https://www.googleapis.com/customsearch/v1"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()