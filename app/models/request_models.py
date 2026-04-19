from pydantic import BaseModel

class SkillRequest(BaseModel):
    persona_id: str
    problem: str