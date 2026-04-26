from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.assessor import get_opening_question, continue_assessment
from routers.parse import sessions

router = APIRouter()

class MessageRequest(BaseModel):
    session_id: str
    user_message: str | None = None   # None = start a new skill

@router.post("/start")
async def start_skill_assessment(body: MessageRequest):
    session = sessions.get(body.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    idx = session.current_skill_index
    if idx >= len(session.skill_states):
        return {"done": True, "message": "All skills assessed."}

    skill_state = session.skill_states[idx]
    skill_state.status = "in_progress"

    opening = get_opening_question(skill_state.skill, session.jd_text)
    skill_state.conversation.append({"role": "assistant", "content": opening})

    return {
        "skill": skill_state.skill,
        "turn": 1,
        "message": opening,
        "done": False,
    }

@router.post("/message")
async def send_message(body: MessageRequest):
    session = sessions.get(body.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    idx = session.current_skill_index
    skill_state = session.skill_states[idx]

    # Append user message
    skill_state.conversation.append({"role": "user", "content": body.user_message})
    skill_state.turns += 1

    reply, score = continue_assessment(
        skill=skill_state.skill,
        jd_text=session.jd_text,
        conversation=skill_state.conversation,
    )

    skill_state.conversation.append({"role": "assistant", "content": reply})

    if score:
        skill_state.score = score
        skill_state.status = "done"
        session.current_skill_index += 1
        all_done = session.current_skill_index >= len(session.skill_states)
        if all_done:
            session.phase = "complete"
        return {
            "message": reply,
            "skill_complete": True,
            "score": score.model_dump(),
            "all_complete": all_done,
        }

    return {
        "message": reply,
        "skill_complete": False,
        "turn": skill_state.turns,
    }