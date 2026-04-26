from fastapi import APIRouter, UploadFile, File, Form
from services.skill_extractor import extract_skills
from services.pdf_parser import extract_text_from_pdf
from models.session import AssessmentSession, SkillAssessmentState
from models.skill import SkillGap
import uuid

router = APIRouter()

# In-memory session store (use Redis in production)
sessions: dict[str, AssessmentSession] = {}

@router.post("/")
async def parse_inputs(
    jd_text: str = Form(...),
    resume_file: UploadFile = File(None),
    resume_text: str = Form(None),
):
    # Handle PDF or plain text resume
    if resume_file:
        raw = await resume_file.read()
        resume = extract_text_from_pdf(raw)
    else:
        resume = resume_text or ""

    result = extract_skills(jd_text, resume)

    session_id = str(uuid.uuid4())
    gaps = [SkillGap(**g) for g in result["gaps"]]
    
    # Only assess skills that are partial or missing
    skills_to_assess = [
        g.skill for g in gaps if g.status != "matched"
    ]

    session = AssessmentSession(
        session_id=session_id,
        gaps=gaps,
        skill_states=[
            SkillAssessmentState(skill=s, status="pending")
            for s in skills_to_assess
        ],
        jd_text=jd_text,
        resume_text=resume,
        phase="pending",
    )
    sessions[session_id] = session

    return {
        "session_id": session_id,
        "required_skills": result["required_skills"],
        "claimed_skills": result["claimed_skills"],
        "gaps": result["gaps"],
        "skills_to_assess": skills_to_assess,
    }