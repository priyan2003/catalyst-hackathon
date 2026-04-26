from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SkillStatus(str, Enum):
    matched = "matched"
    partial = "partial"
    missing = "missing"

class RequiredSkill(BaseModel):
    name: str
    category: str          # e.g. "technical", "soft", "domain"
    importance: int        # 1–5 weight from JD

class ClaimedSkill(BaseModel):
    name: str
    level: str             # e.g. "3 years", "familiar", "expert"
    evidence: str          # raw text from resume

class SkillGap(BaseModel):
    skill: str
    status: SkillStatus
    required_importance: int
    claimed_level: Optional[str] = None

class ProficiencyScore(BaseModel):
    skill: str
    score: float           # 0.0–10.0
    conceptual_depth: float
    practical_application: float
    recency: float
    rationale: str
    transcript: list[dict] # [{role, content}]