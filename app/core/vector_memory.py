import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from typing import List, Dict

class VectorMemory:
    def __init__(self, storage_path: str = "memory_store"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.dimension = 384  # embedding size
        self.index_file = os.path.join(storage_path, "faiss.index")
        self.meta_file = os.path.join(storage_path, "metadata.pkl")

        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata: List[Dict] = []

        self._load()

    def _load(self):
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)

        if os.path.exists(self.meta_file):
            with open(self.meta_file, "rb") as f:
                self.metadata = pickle.load(f)

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "wb") as f:
            pickle.dump(self.metadata, f)

    def add(self, text: str, meta: Dict = None):
        embedding = self.model.encode([text])[0]
        vector = np.array([embedding]).astype("float32")

        self.index.add(vector)

        self.metadata.append({
            "text": text,
            "meta": meta or {}
        })

        self._save()

    def search(self, query: str, top_k: int = 5):
        if len(self.metadata) == 0:
            return []

        query_vec = self.model.encode([query])[0]
        query_vec = np.array([query_vec]).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                results.append({
                    "text": self.metadata[idx]["text"],
                    "meta": self.metadata[idx]["meta"],
                    "score": float(distances[0][i])
                })

        return results

    def clear(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        self._save()

    def size(self):
        return len(self.metadata)