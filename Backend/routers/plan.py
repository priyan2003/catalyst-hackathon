from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.plan_generator import generate_plan
from routers.parse import sessions

router = APIRouter()

class PlanRequest(BaseModel):
    session_id: str
    prioritised_gaps: list[dict]

@router.post("/")
async def create_learning_plan(body: PlanRequest):
    session = sessions.get(body.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    # Extract skills the candidate already has at a decent level
    existing_skills = [
        state.skill for state in session.skill_states
        if state.score and state.score.score >= 6.0
    ]

    plans = generate_plan(body.prioritised_gaps, existing_skills)
    return {"plans": plans}