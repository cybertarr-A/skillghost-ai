import json
import os

class PersonaEngine:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "data", "personas.json")

        with open(file_path, "r") as f:
            self.personas = json.load(f)

    def get_persona(self, persona_id: str):
        return self.personas.get(persona_id, None)