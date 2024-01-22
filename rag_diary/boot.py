import logging
from logging import getLogger

from rag_diary.agent_langchain_basic import AgentLangchainBasic
from rag_diary.config import Config, PathsPrompts
from langchain_openai import OpenAI

from rag_diary.controller import Controller
from rag_diary.vectore_store import VectorStore
from rag_diary.vectore_store_chromadb import VectorStoreChromadb


def boot(config: Config) -> Controller:
    logging.basicConfig(level=config.debug_level)
    logger = getLogger(__name__)
    logger.info("hello Im rag_diary")

    paths_prompts = PathsPrompts.from_yml(config.agent_prompt_mapping_path)

    vector_store: VectorStore = VectorStoreChromadb(
        db_path=config.rag_diary_vector_db_path, collection_name=config.default_db_name
    )

    embedding_model = OpenAI(api_key=config.OPENAI_API_KEY)

    agent_langchain_basic = AgentLangchainBasic(
        llm=embedding_model,
        vector_store=vector_store,
        prompt=paths_prompts.agent_langchain_basic,
        prompt_variables=["prompt"],
    )

    return Controller(vector_store=vector_store, agents=[agent_langchain_basic])
