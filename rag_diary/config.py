from pathlib import Path
import json
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_API_KEY: str
    rag_diary_db_path: Path
    rag_diary_vector_db_path: Path

    agent_prompt_mapping_path: Path
    default_db_name: str = "rag_diary"
    debug_level: str = "INFO"

    class Config:
        env_file = ".env"


class PathsPrompts(BaseSettings):
    agent_langchain_basic: Path

    @classmethod
    def from_yml(cls, path: Path):
        return cls(**json.loads(path.read_text()))
