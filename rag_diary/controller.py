from rag_diary.vectore_store import VectorStore


class Controller:

    def __init__(self, vector_store: VectorStore):
        self.vector_store: VectorStore = vector_store

    def new_entry(self):
        pass

    def query_db(self):
        pass

    def delete_entry(self):
        pass
