from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    LLM_PROVIDER: str = "GEMINI"  # GEMINI or OPENAI
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
