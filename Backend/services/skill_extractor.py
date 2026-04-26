import json
import re
from services.openai_client import chat
from utils.prompts import SKILL_EXTRACTOR_SYSTEM


def extract_json_from_text(text: str):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{[\s\S]*?\}", text)
        if match:
            return json.loads(match.group())
        raise ValueError("No valid JSON found")


def extract_skills(jd_text: str, resume_text: str) -> dict:
    user_message = f"""
JOB DESCRIPTION:
{jd_text}

---

CANDIDATE RESUME:
{resume_text}
"""

    raw = ""  # safety init

    for attempt in range(2):
        raw = chat(
            messages=[{"role": "user", "content": user_message}],
            system=SKILL_EXTRACTOR_SYSTEM,
            max_tokens=3000,
        )

        print(f"\n--- LLM RAW RESPONSE (Attempt {attempt+1}) ---\n{raw}\n")

        try:
            parsed = extract_json_from_text(raw)

            if not isinstance(parsed, dict):
                raise ValueError("Response is not a JSON object")

            # ✅ ensure required keys exist
            parsed.setdefault("required_skills", [])
            parsed.setdefault("claimed_skills", [])
            parsed.setdefault("gaps", [])

            return parsed

        except Exception as e:
            print(f"Parsing failed (Attempt {attempt+1}):", e)

    # ✅ FINAL SAFE FALLBACK (no crash ever)
    return {
        "required_skills": [],
        "claimed_skills": [],
        "gaps": [],
        "error": "Failed to parse LLM response",
        "raw_output": raw
    }