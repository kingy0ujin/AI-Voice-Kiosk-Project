import chromadb
from src.core.config import settings

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(name="menu_items")

    def add_texts(self, texts: list[str], metadatas: list[dict], ids: list[str]):
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
