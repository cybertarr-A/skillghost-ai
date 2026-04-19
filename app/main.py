from fastapi import FastAPI, HTTPException
from app.models.request_models import SkillRequest
from app.core.persona_engine import PersonaEngine
from app.core.reasoning_engine import ReasoningEngine
from app.core.feedback_engine import FeedbackEngine
app = FastAPI(title="SkillGhost AI")

persona_engine = PersonaEngine()
reasoning_engine = ReasoningEngine()
feedback_engine = FeedbackEngine()
    
@app.get("/")
def root():
    return {"message": "SkillGhost AI is running"}

@app.post("/think")
def think(request: SkillRequest):
    persona = persona_engine.get_persona(request.persona_id)

    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    result = reasoning_engine.generate_thinking(persona, request.problem)

    return {
        "persona": persona["name"],
        "thinking": result
    }

@app.post("/practice")
def practice(request: dict):
    problem = request.get("problem")
    solution = request.get("solution")
    user_id = request.get("user_id", "default")

    if not problem or not solution:
        raise HTTPException(status_code=400, detail="Missing fields")

    feedback = feedback_engine.analyze(problem, solution, user_id)

    return {
        "problem": problem,
        "feedback": feedback
    }