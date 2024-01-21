from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

Embedding = List[float]
Records = List[Dict]


@dataclass
class Entry:
    embedding: Embedding
    entry: str
    datetime: datetime
