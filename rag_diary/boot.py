from rag_diary.entry import EntryHandler
from rag_diary.embedding import VectorHandler
from rag_diary.config import Config
from llama_index.embeddings import OpenAIEmbedding


def boot(config: Config):
    embedding_model = OpenAIEmbedding(api_key=config.OPENAI_API_KEY)
    vector_handler = VectorHandler(api_key=config.OPENAI_API_KEY, embedding_model=embedding_model)
    entry_handler = EntryHandler(db=config.rag_diary_db_path, vector_handler=vector_handler)

    return entry_handler
