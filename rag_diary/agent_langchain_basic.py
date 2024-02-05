from logging import getLogger
from pathlib import Path
from typing import List, Dict, Sequence

from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document, BaseDocumentTransformer

from rag_diary.agent import Agent
from rag_diary.types import AgentJob
from rag_diary.vector_store import VectorStore
from langchain.prompts import PromptTemplate
from langchain.llms import BaseLLM
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate


class AgentLangchainBasic(Agent):
    name = "agent_langchain_basic"
    job = AgentJob.retriever

    def __init__(
        self,
        prompts: Dict[str, str],
        vector_store: VectorStore,
        llm: BaseLLM,
        langchain_chroma: Chroma,
        transformer: BaseDocumentTransformer,
    ):
        self.logger = getLogger(__name__)
        self.messages: List[str] = []
        self.vector_store: VectorStore = vector_store
        self.llm: BaseLLM = llm
        self.prompts: Dict[str, str] = prompts

        self.langchain_chroma: Chroma = langchain_chroma

        self.retriever = langchain_chroma.as_retriever()
        self.transformer: BaseDocumentTransformer = transformer

    def transform_docs(self, docs: Sequence[Document]) -> Sequence[Document]:
        return self.transformer.transform_documents(docs)

    def prompt(self, query: Dict):
        docs: Sequence[Document] = self.retriever.get_relevant_documents(query)
        context: Sequence[Document] = self.transform_docs(docs)

        document_variable_name = "context"
        prompt = PromptTemplate(template=self.prompts["llm_chain"], input_variables=["query", document_variable_name])

        document_prompt = PromptTemplate(input_variables=["page_content"], template=self.prompts["document"])

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        chain = StuffDocumentsChain(
            llm_chain=llm_chain, document_prompt=document_prompt, document_variable_name=document_variable_name
        )

        return chain.invoke(
            query=query,
            input={
                "query": "what is the best game",
                "input_documents": context
            })
