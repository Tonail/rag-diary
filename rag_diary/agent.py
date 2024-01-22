from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def prompt(self, prompt: str):
        raise NotImplementedError("Agent must implement prompt()")
