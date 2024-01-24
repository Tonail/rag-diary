from pathlib import Path
import json
from typing import Dict

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_API_KEY: str
    RAG_DIARY_DB_PATH: Path
    RAG_DIARY_CHROMA_DB_PATH: Path

    AGENT_PROMPT_MAPPING_PATH: Path
    DEFAULT_DB_NAME: str = "rag_diary"
    DEBUG_LEVEL: str = "INFO"
    OPENAI_MODEL_NAME: str = "text-embedding-ada-002"

    class Config:
        env_file = ".env"


class PathsPrompts(BaseSettings):
    AGENT_LANGCHAIN_BASIC__LLM_CHAIN: Path
    AGENT_LANGCHAIN_BASIC__DOCUMENT: Path

    @classmethod
    def from_json(cls, path: Path):
        folder: Path = path.parent
        config: Dict = json.loads(path.read_text())
        return cls(**{k.upper(): folder / v for k, v in config.items()})
