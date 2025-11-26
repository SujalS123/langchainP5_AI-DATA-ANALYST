from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "GEMINI")
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
