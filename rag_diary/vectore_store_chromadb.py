from logging import getLogger
from pathlib import Path
from typing import List, Dict
from uuid import uuid4

import chromadb
from chromadb import QueryResult
from chromadb.api.models.Collection import Collection

from rag_diary.types import Embedding, Records
from rag_diary.vectore_store import VectorStore


class ChromadbVectorStore(VectorStore):

    def __init__(self, db_path: Path, collection_name: str):
        self.logger = getLogger(__name__)
        self.db_path: Path = db_path
        self.client: chromadb.PersistentClient = chromadb.PersistentClient(path=str(db_path.absolute()))
        self._check_heartbeat()

        self.collection: Collection = self._get_collection(collection_name)

    def _get_collection(self, collection_name: str) -> chromadb.Collection:
        try:
            return self.client.get_collection(collection_name)
        except ValueError as err:
            self.logger.warning(err)
            self.logger.info("getting new collection")
            return self.client.create_collection(collection_name)

    def _check_heartbeat(self):
        beat = self.client.heartbeat()
        self.logger.debug(f"chromadb:{self.db_path} heartbeat: {beat}")

    @staticmethod
    def _query_results_as_records(result: QueryResult) -> Records:
        return [{
            "document": document,
            "_id": result.get("ids", [])[0][index],
            **result.get("metadatas", [])[0][index]
        } for index, document in enumerate(result["documents"][0])]

    def add(self, document: str, metadata: dict):
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[str(uuid4())]
        )

    def add_multiple(self, documents: List[str], metadatas: List[dict]):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=[str(uuid4()) for _ in range(len(documents))]
        )

    def delete(self, record_id: str):
        self.collection.delete(ids=[record_id])

    def delete_multiple(self, record_ids: List[str]):
        self.collection.delete(ids=record_ids)

    def query_by_str(self, query: str) -> Records:
        result = self.collection.query(
            query_texts=query
        )
        return self._query_results_as_records(result)

    def query_by_embedding(self, query: Embedding) -> Records:
        result = self.collection.query(
            query_embeddings=query
        )
        return self._query_results_as_records(result)

    def query_by_image(self, query) -> Records:
        raise NotImplementedError("query_by_image not implemented")
