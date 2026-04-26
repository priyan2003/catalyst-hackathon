from fastapi import APIRouter, HTTPException
from services.gap_analyser import analyse_gaps
from routers.parse import sessions

router = APIRouter()

@router.get("/{session_id}")
async def get_gap_analysis(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    if session.phase != "complete":
        raise HTTPException(400, "Assessment not yet complete")

    scores = [
        state.score for state in session.skill_states
        if state.score is not None
    ]
    ranked = analyse_gaps(session.gaps, scores, session.jd_text)
    return {"ranked_gaps": ranked}