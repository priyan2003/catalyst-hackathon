import json
import re
from services.openai_client import chat, stream_chat
from utils.prompts import ASSESSOR_SYSTEM
from models.skill import ProficiencyScore

ASSESSMENT_COMPLETE_TAG = "[ASSESSMENT_COMPLETE]"


# ---------------------------
# BUILD SYSTEM PROMPT
# ---------------------------
def build_system(skill: str, jd_context: str) -> str:
    return (
        ASSESSOR_SYSTEM
        + f"\n\nSkill being assessed: {skill}"
        + f"\nJob context: {jd_context[:500]}"
    )


# ---------------------------
# OPENING QUESTION
# ---------------------------
def get_opening_question(skill: str, jd_text: str) -> str:
    system = build_system(skill, jd_text)
    return chat(
        messages=[{"role": "user", "content": f"Please begin the assessment for: {skill}"}],
        system=system,
    )


# ---------------------------
# SAFE JSON EXTRACTOR
# ---------------------------
def extract_json(text: str):
    """
    Extracts the LAST valid JSON object from LLM output.
    Handles messy responses (extra text, markdown, etc.)
    """
    matches = re.findall(r"\{[\s\S]*?\}", text)  # non-greedy

    for m in reversed(matches):
        try:
            return json.loads(m)
        except:
            continue

    return None


# ---------------------------
# MAIN ASSESSMENT FLOW
# ---------------------------
def continue_assessment(
    skill: str,
    jd_text: str,
    conversation: list[dict]
) -> tuple[str, ProficiencyScore | None]:
    """
    Returns (next_question_or_message, score_if_complete)
    """
    system = build_system(skill, jd_text)
    response = chat(messages=conversation, system=system)

    # Debug log (IMPORTANT for troubleshooting)
    print("\n--- RAW LLM RESPONSE ---\n", response, "\n")

    if ASSESSMENT_COMPLETE_TAG in response:

        data = extract_json(response)

        if data:
            try:
                score = ProficiencyScore(
                    skill=skill,
                    score=float(data.get("score", 0)),
                    conceptual_depth=float(data.get("conceptual_depth", 0)),
                    practical_application=float(data.get("practical_application", 0)),
                    recency=float(data.get("recency", 0)),
                    rationale=data.get("rationale", ""),
                    transcript=conversation,
                )

                print("✅ PARSED SCORE:", score)
                return "Thank you — assessment for this skill is complete.", score

            except Exception as e:
                print("❌ SCORE CONSTRUCTION FAILED:", e)

        # If parsing failed
        print("❌ JSON PARSE FAILED. RESPONSE:\n", response)

        # Return fallback (prevents UI from showing all 0 silently)
        fallback = ProficiencyScore(
            skill=skill,
            score=1,
            conceptual_depth=1,
            practical_application=1,
            recency=1,
            rationale="Parsing failed — fallback score applied",
            transcript=conversation,
        )
        return "Assessment completed (with fallback scoring).", fallback

    return response, None