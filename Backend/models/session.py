from pydantic import BaseModel
from typing import Optional
from models.skill import SkillGap, ProficiencyScore
from enum import Enum

class SessionPhase(str, Enum):
    pending = "pending"
    assessing = "assessing"
    complete = "complete"

class SkillAssessmentState(BaseModel):
    skill: str
    status: str            # "pending" | "in_progress" | "done"
    turns: int = 0
    score: Optional[ProficiencyScore] = None
    conversation: list[dict] = []

class AssessmentSession(BaseModel):
    session_id: str
    phase: SessionPhase = SessionPhase.pending
    gaps: list[SkillGap] = []
    skill_states: list[SkillAssessmentState] = []
    current_skill_index: int = 0
    jd_text: str = ""
    resume_text: str = ""