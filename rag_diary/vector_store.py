from abc import ABC, abstractmethod
from typing import List, Optional

from rag_diary.types import Embedding


class VectorStore(ABC):
    @abstractmethod
    def add(self, document: str, metadata: dict, embedding: Optional[Embedding] = None) -> None:
        raise NotImplementedError("Add not implemented")

    @abstractmethod
    def add_multiple(self, documents: List[str], metadatas: List[dict], embeddings: Optional[List[Embedding]] = None):
        raise NotImplementedError("Add not implemented")

    @abstractmethod
    def delete(self, record_id, *args, **kwargs):
        raise NotImplementedError("Delete not implemented")

    def delete_multiple(self, record_ids, *args, **kwargs):
        raise NotImplementedError("Delete not implemented")

    @abstractmethod
    def query_by_str(self, query: str):
        raise NotImplementedError("Query not implemented")

    @abstractmethod
    def query_by_embedding(self, query: Embedding):
        raise NotImplementedError("Query not implemented")

    @abstractmethod
    def query_by_image(self, query: str):
        raise NotImplementedError("Query not implemented")
