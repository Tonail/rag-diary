from typing import List

import openai
from llama_index.core.embeddings.base import BaseEmbedding


class VectorHandler:
    def __init__(self, api_key: str, embedding_model: BaseEmbedding):
        self.api_key = api_key
        self.embedding_model = embedding_model
        openai.api_key = api_key

    def generate_embedding(self, text) -> List[float]:
        return self.embedding_model.get_text_embedding(text)
