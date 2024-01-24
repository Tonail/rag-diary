from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from datetime import datetime
from uuid import uuid4

Embedding = List[float]
Records = List[Dict]


class AgentJob(Enum):
    retriever = 0

@dataclass
class Entry:
    entry: str
    timestamp: int
    entry_id: str

    @classmethod
    def new_entry(cls, entry: str):
        now = datetime.utcnow()
        return cls(entry=entry, timestamp=int(now.timestamp()), entry_id=str(uuid4()))
