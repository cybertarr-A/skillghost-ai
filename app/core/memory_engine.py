import json
import os
from typing import List, Dict

from app.core.vector_memory import VectorMemory


class MemoryEngine:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.file_path = os.path.join(base_path, "data", "user_memory.json")

        # 🔥 Vector Memory Init
        self.vector_memory = VectorMemory(
            storage_path=os.path.join(base_path, "data", "vector_memory")
        )

        # Ensure JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    # =========================
    # JSON MEMORY (STRUCTURED)
    # =========================

    def load_memory(self) -> Dict:
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_memory(self, data: Dict):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    # =========================
    # STORE MEMORY (HYBRID)
    # =========================

    def update_user(self, user_id: str, feedback: str):
        data = self.load_memory()

        if user_id not in data:
            data[user_id] = {
                "mistakes": [],
                "history": []
            }

        # Store raw feedback
        data[user_id]["history"].append(feedback)

        # 🔥 VECTOR MEMORY STORAGE
        self.vector_memory.add(
            text=feedback,
            meta={"user_id": user_id, "type": "feedback"}
        )

        # =========================
        # PATTERN DETECTION
        # =========================

        text = feedback.lower()

        # Scalability
        if any(word in text for word in ["scale", "scalable", "scalability", "load", "traffic"]):
            data[user_id]["mistakes"].append("scalability")

        # Security
        if any(word in text for word in ["security", "vulnerability", "attack", "auth", "token", "password"]):
            data[user_id]["mistakes"].append("security")

        # Validation
        if any(word in text for word in ["validation", "input", "sanitize", "check", "verify"]):
            data[user_id]["mistakes"].append("validation")

        # Architecture
        if any(word in text for word in ["monolith", "coupling", "architecture", "design", "service"]):
            data[user_id]["mistakes"].append("architecture")

        self.save_memory(data)

    # =========================
    # VECTOR SEARCH (NEW)
    # =========================

    def semantic_search(self, query: str, user_id: str = None, top_k: int = 5) -> List[Dict]:
        results = self.vector_memory.search(query, top_k=top_k)

        # Optional filter by user
        if user_id:
            results = [r for r in results if r["meta"].get("user_id") == user_id]

        return results

    # =========================
    # USER INSIGHTS (IMPROVED)
    # =========================

    def get_user_insights(self, user_id: str) -> str:
        data = self.load_memory()

        if user_id not in data:
            return "No history yet."

        mistakes = data[user_id]["mistakes"]

        if not mistakes:
            return "No clear weaknesses detected yet."

        # Count patterns
        summary = {}
        for m in mistakes:
            summary[m] = summary.get(m, 0) + 1

        insights = sorted(summary.items(), key=lambda x: x[1], reverse=True)

        formatted = ", ".join([f"{k} ({v})" for k, v in insights[:3]])

        return f"Common weaknesses: {formatted}"

    # =========================
    # CONTEXT BUILDER (🔥 NEW)
    # =========================

    def build_context(self, query: str, user_id: str = None) -> str:
        memories = self.semantic_search(query, user_id=user_id, top_k=3)

        if not memories:
            return ""

        return "\n".join([m["text"] for m in memories])