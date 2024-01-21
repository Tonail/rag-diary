from typing import List

import openai
from llama_index.core.embeddings.base import BaseEmbedding


from rag_diary.types import Embedding

# @todo deprecate this for VectorStore Objects
class VectorHandler:
    def __init__(self, api_key: str, embedding_model: BaseEmbedding):
        self.api_key = api_key
        self.embedding_model = embedding_model
        openai.api_key = api_key

    def generate_embedding(self, text) -> Embedding:
        return self.embedding_model.get_text_embedding(text)
