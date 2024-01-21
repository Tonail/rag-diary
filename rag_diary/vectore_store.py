from abc import ABC, abstractmethod
from typing import List

from rag_diary.types import Embedding


class VectorStore(ABC):

    @abstractmethod
    def _check_heartbeat(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, document: str, metadata: dict):
        raise NotImplementedError

    @abstractmethod
    def add_multiple(self, documents: List[str], metadatas: List[dict]):
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id, *args, **kwargs):
        raise NotImplementedError

    def delete_multiple(self, record_ids, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def query_by_str(self, query: str):
        raise NotImplementedError

    @abstractmethod
    def query_by_embedding(self, query: Embedding):
        raise NotImplementedError

    @abstractmethod
    def query_by_image(self, query: str):
        raise NotImplementedError