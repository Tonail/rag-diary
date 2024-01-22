from logging import getLogger
from pathlib import Path
from typing import List, Dict
from rag_diary.agent import Agent
from rag_diary.vectore_store import VectorStore
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import BaseLLM


class AgentLangchainBasic(Agent):
    def __init__(self, prompt: Path, prompt_variables: List[str], vector_store: VectorStore, llm: BaseLLM):
        self.logger = getLogger(__name__)
        self.messages: List[str] = []
        self.vector_store: VectorStore = vector_store
        self.llm: BaseLLM = llm
        self.prompt_path: Path = prompt
        self.prompt_variables: List[str] = prompt_variables

    def get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate(
            input_variables=self.prompt_variables,
            template=self.prompt_path.read_text(),
        )

    def prompt(self, prompt: Dict):
        llm_chain = LLMChain(llm=self.llm, prompt=self.get_prompt_template())
        llm_chain.run(prompt)
