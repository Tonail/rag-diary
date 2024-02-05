from logging import getLogger
from typing import List, Dict

from rag_diary.agent import Agent
from rag_diary.vector_store import VectorStore
from rag_diary.types import Entry, AgentJob


class Controller:
    def __init__(self, vector_store: VectorStore):
        self.vector_store: VectorStore = vector_store
        self.agents: Dict[str, Agent] = {}
        self.logger = getLogger(__name__)

    def new_entry(self, entry: str):
        return self.vector_store.add_multiple(documents=[entry], metadatas=[Entry.new_entry(entry).__dict__])

    def query_db(self, query: str):
        return self.vector_store.query_by_str(query=query)

    def register_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def query_retriever_agent(self, query: str):
        retrievers = [agent for agent in self.agents.values() if agent.job == AgentJob.retriever]
        results = []
        if retrievers:
            for retriever in retrievers:
                result = retriever.prompt(query=query)
                results.append(result)
        return results


