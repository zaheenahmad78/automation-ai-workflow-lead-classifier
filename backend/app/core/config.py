from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str = "sqlite:///./leads.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()