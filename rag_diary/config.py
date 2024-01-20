from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_API_KEY: str
    rag_diary_db_path: Path

    class Config:
        env_file = ".env"
