import logging
from logging import getLogger

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain_community.document_transformers import LongContextReorder
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.embeddings import Embeddings

from rag_diary.agent_langchain_basic import AgentLangchainBasic
from rag_diary.config import Config, PathsPrompts

from langchain_openai.llms import OpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

from rag_diary.controller import Controller
from rag_diary.vectore_store import VectorStore
from rag_diary.vectore_store_chromadb import VectorStoreChromadb, get_chromadb_collection


def boot(config: Config) -> Controller:
    logging.basicConfig(level=config.DEBUG_LEVEL)
    logger = getLogger(__name__)
    logger.info("hello Im rag_diary")

    paths_prompts: PathsPrompts = PathsPrompts.from_json(config.AGENT_PROMPT_MAPPING_PATH)

    #
    # Construct vector store
    #
    embedding_function = OpenAIEmbeddingFunction(api_key=config.OPENAI_API_KEY, model_name=config.OPENAI_MODEL_NAME)
    client = chromadb.PersistentClient(path=str(config.RAG_DIARY_CHROMA_DB_PATH.absolute()))
    collection = get_chromadb_collection(
        client, collection_name=config.DEFAULT_DB_NAME, embedding_function=embedding_function
    )
    vector_store: VectorStore = VectorStoreChromadb(client=client, collection=collection)

    #
    # Construct Agents
    #

    # Boot basic retriever agent
    llm = OpenAI(api_key=config.OPENAI_API_KEY)
    langchain_embeddings: Embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
    langchain_chroma: Chroma = Chroma(
        client=client,
        collection_name=config.DEFAULT_DB_NAME,
        embedding_function=langchain_embeddings,
        persist_directory=str(config.RAG_DIARY_CHROMA_DB_PATH.absolute()),
    )
    agent_langchain_basic = AgentLangchainBasic(
        llm=llm,
        vector_store=vector_store,
        prompts={
            "llm_chain": paths_prompts.AGENT_LANGCHAIN_BASIC__LLM_CHAIN.read_text(),
            "document": paths_prompts.AGENT_LANGCHAIN_BASIC__DOCUMENT.read_text()
        },
        langchain_chroma=langchain_chroma,
        transformer=LongContextReorder(),
    )
    controller = Controller(vector_store=vector_store)
    controller.register_agent(agent_langchain_basic)

    return controller
