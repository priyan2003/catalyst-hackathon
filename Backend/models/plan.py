from pydantic import BaseModel

class Resource(BaseModel):
    title: str
    url: str
    type: str              # "course" | "docs" | "book" | "project"
    duration: str          # e.g. "6 hours"
    free: bool

class LearningStage(BaseModel):
    name: str              # "Foundation" | "Application" | "Mastery"
    goal: str
    resources: list[Resource]
    estimated_weeks: int
    milestone: str         # what "done" looks like

class SkillPlan(BaseModel):
    skill: str
    gap_score: float
    adjacent_skills: list[str]  # skills already known that help
    total_weeks: int
    stages: list[LearningStage]

class LearningPlan(BaseModel):
    session_id: str
    prioritised_skills: list[SkillPlan]
    total_estimated_weeks: int
    summary: str