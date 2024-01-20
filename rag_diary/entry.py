from datetime import datetime
from pathlib import Path
from typing import Optional, List
import pandas as pd

from rag_diary.embedding import VectorHandler
from rag_diary.utils import guard_file_existence

# from rag_diary.types import Embedding


class EntryHandler:
    def __init__(self, db: Path, vector_handler: VectorHandler):
        try:
            guard_file_existence(db)
        except FileNotFoundError:
            pd.DataFrame().to_parquet(db)

        self.db_location = db
        self.vector_handler = vector_handler

    def _generate_embedding(self, entry: str) -> List[float]:
        return self.vector_handler.generate_embedding(entry)

    def add_entry(self, new_entry):
        # Read existing parquet file
        df = pd.read_parquet(self.db_location)

        record = {"embedding": self._generate_embedding(new_entry), "entry": new_entry, "timestamp": datetime.utcnow()}

        # Append new entry to the DataFrame
        new_df = pd.DataFrame([record])
        df = pd.concat([df, new_df])

        # Save the updated DataFrame to the parquet file
        df.to_parquet(self.db_location)

    def add_new_entry_from_file(self, file_path: Path):
        guard_file_existence(file_path)
        self.add_entry(file_path.read_text())
