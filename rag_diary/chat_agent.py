from typing import List

from rag_diary.types import Embedding


class ChatAgent:

    def __init__(self):
        self.messages: List[str] = []
        self.context: List[Embedding] = []

