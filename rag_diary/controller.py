from typing import List

from rag_diary.agent import Agent
from rag_diary.vectore_store import VectorStore
from rag_diary.types import Entry


class Controller:
    def __init__(self, vector_store: VectorStore, agents: List[Agent]):
        self.vector_store: VectorStore = vector_store
        self.agents: List[Agent] = agents

    def new_entry(self, entry: str):
        return self.vector_store.add_multiple(documents=[entry], metadatas=[Entry.new_entry(entry).__dict__])

    def query_db(self, query: str):
        return self.vector_store.query_by_str(query=query)

    def delete_entry(self):
        pass
