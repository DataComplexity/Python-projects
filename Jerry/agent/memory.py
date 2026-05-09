import chromadb
from chromadb.config import Settings
import hashlib
import os
from datetime import datetime

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "memory")

class MemoryManager:
    def __init__(self):
        os.makedirs(MEMORY_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=MEMORY_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="jerry_memory",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"[MEMORY] Loaded {self.collection.count()} memory entries.")

    def save(self, user_input: str, response: str):
        doc_id = hashlib.md5(f"{user_input}{datetime.now()}".encode()).hexdigest()
        combined = f"User: {user_input}\nJerry: {response}"
        self.collection.add(
            documents=[combined],
            ids=[doc_id],
            metadatas=[{"timestamp": datetime.now().isoformat(), "type": "conversation"}]
        )

    def get_relevant(self, query: str, n=3) -> str:
        if self.collection.count() == 0:
            return ""
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n, self.collection.count())
        )
        docs = results.get("documents", [[]])[0]
        return "\n---\n".join(docs) if docs else ""

    def count(self) -> int:
        return self.collection.count()

    def clear(self):
        self.client.delete_collection("jerry_memory")
        self.collection = self.client.get_or_create_collection("jerry_memory")
        print("[MEMORY] Memory cleared.")

    def save_preference(self, key: str, value: str):
        doc_id = f"pref_{key}"
        try:
            self.collection.delete(ids=[doc_id])
        except:
            pass
        self.collection.add(
            documents=[f"User preference — {key}: {value}"],
            ids=[doc_id],
            metadatas=[{"type": "preference", "key": key}]
        )

    def get_preferences(self) -> list:
        results = self.collection.get(where={"type": "preference"})
        return results.get("documents", [])
