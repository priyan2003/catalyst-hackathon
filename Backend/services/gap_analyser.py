import json
from services.openai_client import chat
from utils.prompts import GAP_ANALYSER_SYSTEM
from models.skill import ProficiencyScore, SkillGap

def analyse_gaps(
    gaps: list[SkillGap],
    scores: list[ProficiencyScore],
    jd_text: str
) -> list[dict]:
    scores_summary = {
        s.skill: {"score": s.score, "rationale": s.rationale}
        for s in scores
    }
    payload = {
        "gaps": [g.model_dump() for g in gaps],
        "proficiency_scores": scores_summary,
        "jd_context": jd_text[:800],
    }
    raw = chat(
        messages=[{"role": "user", "content": json.dumps(payload)}],
        system=GAP_ANALYSER_SYSTEM,
        max_tokens=3000,
    )
    return json.loads(raw)