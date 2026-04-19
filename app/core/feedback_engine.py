# app/core/feedback_engine.py

from app.services.groq_client import GroqClient
from app.core.memory_engine import MemoryEngine


class FeedbackEngine:
    def __init__(self):
        self.llm = GroqClient()
        self.memory = MemoryEngine()

    def analyze(self, problem: str, user_solution: str, user_id: str = "default") -> str:
        prompt = f"""
You are a senior engineer reviewing a solution.

Be strict, concise, and practical.

---

Problem:
{problem}

User Solution:
{user_solution}

---

Output STRICTLY:

Mistakes:
- max 3 critical issues

Missing:
- max 3 missing concepts

Expert Fix:
- concise correction

Skill Gap:
- short explanation
"""

        # 🔹 Generate response
        response = self.llm.generate(prompt)

        # 🔥 CLEAN OUTPUT (INSIDE FUNCTION)
        cleaned = (
            response.replace("\\n", "\n")
                    .replace("\n\n", "\n")
                    .strip()
        )

        # 🔹 Update memory
        self.memory.update_user(user_id, cleaned)

        # 🔹 Get insights
        insights = self.memory.get_user_insights(user_id)

        # 🔹 Final response
        return f"{cleaned}\n\n🧠 Memory Insight:\n{insights}"