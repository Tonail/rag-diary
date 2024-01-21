from datetime import datetime
from pathlib import Path
import pandas as pd

from rag_diary.embedding import VectorHandler
from rag_diary.utils import guard_file_existence

from rag_diary.types import Embedding, Entry


# @todo entry handler should take in a VectorStore and use it to handle data entry. This should not handle file storage.
class EntryHandler:
    def __init__(self, db: Path, vector_handler: VectorHandler):
        try:
            guard_file_existence(db)
        except FileNotFoundError:
            pd.DataFrame().to_parquet(db)

        self.db_location = db
        self.vector_handler = vector_handler

    def _generate_embedding(self, entry: str) -> Embedding:
        return self.vector_handler.generate_embedding(entry)

    def new_record(self, entry_text: str) -> Entry:
        return Entry(
            embedding=self._generate_embedding(entry_text),
            entry=entry_text,
            datetime=datetime.utcnow()
        )

    def add_entry(self, new_entry):
        df = pd.read_parquet(self.db_location)
        new_df = pd.DataFrame([self.new_record(new_entry).__dict__])
        df = pd.concat([df, new_df])
        df.to_parquet(self.db_location)

    def add_new_entry_from_file(self, file_path: Path):
        guard_file_existence(file_path)
        self.add_entry(file_path.read_text())
