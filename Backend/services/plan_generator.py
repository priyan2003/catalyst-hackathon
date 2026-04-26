import json
import re
from services.openai_client import chat
from utils.prompts import PLAN_GENERATOR_SYSTEM


# ---------------------------
# SAFE JSON PARSER (ARRAY FIRST)
# ---------------------------
def safe_json_parse(text: str):
    # 1. direct parse
    try:
        return json.loads(text)
    except:
        pass

    # 2. extract array
    matches = re.findall(r"\[[\s\S]*\]", text)
    for m in reversed(matches):
        try:
            return json.loads(m)
        except:
            continue

    # 3. 🔥 TRUNCATION FIX (VERY IMPORTANT)
    if "[" in text:
        try:
            partial = text[text.index("["):]
            # close brackets if missing
            open_brackets = partial.count("[")
            close_brackets = partial.count("]")
            partial += "]" * (open_brackets - close_brackets)
            return json.loads(partial)
        except:
            pass

    return None


# ---------------------------
# MAIN FUNCTION
# ---------------------------
def generate_plan(
    prioritised_gaps: list[dict],
    candidate_skills: list[str]
) -> list[dict]:

    user_msg = f"""
Candidate's existing skills: {', '.join(candidate_skills)}

Skills to build learning plans for (in priority order):
{json.dumps(prioritised_gaps[:5], indent=2)}

IMPORTANT:
Return STRICTLY this format:

[
  {{
    "skill": "string",
    "stages": [
      {{
        "name": "string",
        "goal": "string",
        "estimated_weeks": number,
        "milestone": "string",
        "resources": [
          {{
            "title": "string",
            "url": "string",
            "type": "string",
            "duration": "string",
            "free": boolean
          }}
        ]
      }}
    ]
  }}
]

Return ONLY JSON. No explanation.
"""

    raw = ""

    for attempt in range(2):
        raw = chat(
            messages=[{"role": "user", "content": user_msg}],
            system=PLAN_GENERATOR_SYSTEM,
            max_tokens=2000   # 🔥 FIXED (was 800 → causing truncation)
        )

        print(f"\n--- PLAN RAW RESPONSE (Attempt {attempt+1}) ---\n{raw}\n")

        parsed = safe_json_parse(raw)

        # ✅ SIMPLE VALIDATION (don’t over-restrict)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed

        print("⚠️ Parse failed, retrying...")

    # 🔥 FINAL DEBUG
    print("❌ FINAL FAILURE RAW OUTPUT:\n", raw)

    return []