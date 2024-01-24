from abc import ABC, abstractmethod


class Agent(ABC):
    name: str
    job: str

    @abstractmethod
    def prompt(self, query: str):
        raise NotImplementedError("Agent must implement prompt()")
