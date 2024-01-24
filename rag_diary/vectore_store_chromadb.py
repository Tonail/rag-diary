from logging import getLogger
from pathlib import Path
from typing import List, Dict
from uuid import uuid4

import chromadb
from chromadb import QueryResult, EmbeddingFunction
from chromadb.api.models.Collection import Collection

from rag_diary.types import Embedding, Records
from rag_diary.vectore_store import VectorStore


class VectorStoreChromadb(VectorStore):
    def __init__(self, client: chromadb.ClientAPI, collection: chromadb.Collection):
        self.logger = getLogger(__name__)
        self.client: chromadb.ClientAPI = client
        self._check_heartbeat()
        self.collection = collection

    def _check_heartbeat(self):
        beat = self.client.heartbeat()
        self.logger.debug(f"chromadb heartbeat: {beat}")

    @staticmethod
    def _query_results_as_records(result: QueryResult) -> Records:
        return [
            {"document": document, "_id": result.get("ids", [])[0][index], **result.get("metadatas", [])[0][index]}
            for index, document in enumerate(result["documents"][0])
        ]

    def add(self, document: str, metadata: dict, **kwargs):
        self.collection.add(documents=[document], metadatas=[metadata], ids=[str(uuid4())])

    def add_multiple(self, documents: List[str], metadatas: Records, **kwargs):
        self.collection.add(documents=documents, metadatas=metadatas, ids=[str(uuid4()) for _ in range(len(documents))])

    def delete(self, record_id: str, **kwargs):
        self.collection.delete(ids=[record_id])

    def delete_multiple(self, record_ids: List[str], **kwargs):
        self.collection.delete(ids=record_ids)

    def query_by_str(self, query: str) -> Records:
        result = self.collection.query(query_texts=query)
        return self._query_results_as_records(result)

    def query_by_embedding(self, query: Embedding) -> Records:
        result = self.collection.query(query_embeddings=query)
        return self._query_results_as_records(result)

    def query_by_image(self, query) -> Records:
        raise NotImplementedError("query_by_image not implemented")


def get_chromadb_collection(
    client: chromadb.ClientAPI, collection_name: str, embedding_function: chromadb.EmbeddingFunction
) -> chromadb.Collection:
    try:
        return client.get_collection(collection_name)
    except ValueError:
        return client.create_collection(collection_name, embedding_function=embedding_function)
