from app.core.prompt_builder import build_expert_prompt
from app.services.groq_client import GroqClient

class ReasoningEngine:
    def __init__(self):
        self.llm = GroqClient()

    def generate_thinking(self, persona, user_input):
        prompt = build_expert_prompt(persona, user_input)
        return self.llm.generate(prompt)