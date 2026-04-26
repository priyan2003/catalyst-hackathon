# ⬡ Catalyst — AI Skill Assessment & Personalised Learning Agent

> **A resume tells you what someone claims to know — not how well they actually know it.**
> Catalyst takes a Job Description and a candidate's resume, conversationally assesses real proficiency on each required skill, identifies gaps, and generates a personalised learning plan with curated resources and time estimates.

---

## 📌 Table of Contents

- [What is Catalyst?](#-what-is-catalyst)
- [How it Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Setup](#-local-setup)
- [Environment Variables](#-environment-variables)
- [Running the App](#-running-the-app)
- [API Reference](#-api-reference)
- [Common Errors & Fixes](#-common-errors--fixes)
- [Contributing](#-contributing)

---

## 🧠 What is Catalyst?

Catalyst is an **AI-powered skill assessment agent** built for the hiring process. It solves a fundamental problem: traditional hiring relies on resumes, which are self-reported and often inflated.

Catalyst fixes this by:

1. **Parsing** the Job Description to extract all required skills with importance weights
2. **Parsing** the candidate's resume to extract claimed skills with evidence
3. **Identifying gaps** — which skills are matched, partially matched, or missing entirely
4. **Conversationally assessing** each gap skill through a dynamic 3–5 turn interview (not a quiz — a real dialogue that probes depth, edge cases, and practical experience)
5. **Scoring** each skill across three dimensions: Conceptual Depth, Practical Application, and Recency
6. **Generating a ranked learning plan** with adjacent skill detection, time estimates, and curated real resources

---

## ⚙️ How it Works

```
JD + Resume
    │
    ▼
┌─────────────────────────┐
│   Skill Extraction      │  GPT-4o reads JD + resume → structured JSON
│   (OpenAI GPT-4o)       │  required skills, claimed skills, gap status
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Gap Classifier        │  matched / partial / missing
│                         │  only partial + missing go to assessment
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Conversational         │  3–5 turn dynamic dialogue per skill
│  Assessor (GPT-4o)      │  scores: conceptual, practical, recency
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Gap Analyser          │  ranks gaps by severity × learnability
│                         │  detects adjacent skills candidate has
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Learning Plan          │  3-stage path per skill (Foundation →
│  Generator (GPT-4o)     │  Application → Mastery) with real URLs
└────────────┬────────────┘
             │
             ▼
     Personalised Report
  (Heatmap + Scores + Plan)
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI** | OpenAI GPT-4o (`gpt-4o`) |
| **PDF Parsing** | pdfplumber |
| **Frontend** | Vanilla HTML + CSS + JavaScript (single file, no build step) |

---

## 📁 Project Structure

```
catalyst/                          ← Git root
│
├── backend/                       ← All Python source code
│   ├── main.py                    ← FastAPI app, routes, static serving
│   ├── requirements.txt           ← Python dependencies
│   ├── .env                       ← Local secrets (never committed)
│   │
│   ├── static/
│   │   └── index.html             ← Complete frontend (single HTML file)
│   │
│   ├── routers/                   ← FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── parse.py               ← POST /api/parse  — JD + resume ingestion
│   │   ├── assess.py              ← POST /api/assess/start, /api/assess/message
│   │   ├── gaps.py                ← GET  /api/gaps/{session_id}
│   │   └── plan.py                ← POST /api/plan
│   │
│   ├── services/                  ← Business logic layer
│   │   ├── __init__.py
│   │   ├── openai_client.py       ← OpenAI SDK wrapper (chat, stream)
│   │   ├── skill_extractor.py     ← JD + resume → structured skills JSON
│   │   ├── assessor.py            ← Conversational assessment logic
│   │   ├── gap_analyser.py        ← Gap scoring + adjacency mapping
│   │   ├── plan_generator.py      ← Learning plan generation
│   │   └── pdf_parser.py          ← PDF bytes → plain text
│   │
│   ├── models/                    ← Pydantic data models
│   │   ├── __init__.py
│   │   ├── skill.py               ← Skill, SkillGap, ProficiencyScore
│   │   ├── session.py             ← AssessmentSession state machine
│   │   └── plan.py                ← LearningPlan, Resource, Milestone
│   │
│   └── utils/
│       ├── __init__.py
│       └── prompts.py             ← All GPT system prompts in one place
│
├── .gitignore                     ← Excludes .env, __pycache__, venv
└── README.md                      ← This file
```

---

## 💻 Local Setup

Follow these steps exactly to run Catalyst on your machine.

### Prerequisites

Make sure you have these installed before starting:

- **Python 3.11+** — verify with `python --version`
- **pip** — verify with `pip --version`
- **Git** — verify with `git --version`
- **An OpenAI API key** — get one at [platform.openai.com](https://platform.openai.com)

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/catalyst.git
cd catalyst
```

---

### Step 2 — Create a virtual environment

Always use a virtual environment to isolate dependencies from the rest of your system.

```bash
# Create the virtual environment
python -m venv venv

# Activate it — Mac / Linux:
source venv/bin/activate

# Activate it — Windows (Command Prompt):
venv\Scripts\activate.bat

# Activate it — Windows (PowerShell):
venv\Scripts\Activate.ps1
```

You will see `(venv)` at the start of your terminal prompt once it is active. Always confirm this before running any pip or uvicorn commands below.

---

### Step 3 — Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, OpenAI SDK, pdfplumber, and all other required packages. Takes about 30–60 seconds.

Verify the install completed successfully:

```bash
pip show fastapi openai pdfplumber uvicorn
```

Each package should print its name, version, and location. If any are missing, install them individually:

```bash
pip install <package-name>
```

---

### Step 4 — Set up environment variables

Create a `.env` file inside the `backend/` folder:

```bash
# Make sure you are inside backend/
touch .env
```

Open `.env` in any text editor and add:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

> ⚠️ **Never commit this file to Git.** It is already in `.gitignore`. If you accidentally push your API key, revoke it immediately at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and generate a new one.

**How to get your OpenAI API key:**
1. Go to [platform.openai.com](https://platform.openai.com) and sign in
2. Click your profile icon (top right) → **API Keys**
3. Click **+ Create new secret key**
4. Give it a name like `catalyst-local` and click Create
5. Copy the key immediately — it will not be shown again
6. Paste it into your `.env` file

> 💡 GPT-4o costs a small amount per request. A full end-to-end Catalyst assessment (parse + assess + gaps + plan) typically uses $0.05–$0.15 in tokens. Add $5–$10 of credits at [platform.openai.com/settings/billing](https://platform.openai.com/settings/billing) which is more than enough for a hackathon.

---

### Step 5 — Confirm `requirements.txt` uses OpenAI

Open `backend/requirements.txt` and make sure it contains `openai`, not `anthropic`:

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
openai==1.35.0
python-multipart==0.0.12
pdfplumber==0.11.4
pydantic==2.9.0
python-dotenv==1.0.1
httpx==0.27.0
aiofiles==24.1.0
```

If `anthropic` is listed, remove it and replace with `openai==1.35.0`, then re-run `pip install -r requirements.txt`.

---

### Step 6 — Confirm `openai_client.py` is correct

Open `backend/services/openai_client.py` and make sure it looks like this:

```python
from openai import OpenAI
import os

_client = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client

def chat(
    messages: list[dict],
    system: str,
    max_tokens: int = 2000,
) -> str:
    client = get_client()
    all_messages = [{"role": "system", "content": system}] + messages
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=max_tokens,
        messages=all_messages,
    )
    return response.choices[0].message.content

def stream_chat(messages: list[dict], system: str):
    """Generator that yields text chunks for streaming."""
    client = get_client()
    all_messages = [{"role": "system", "content": system}] + messages
    with client.chat.completions.stream(
        model="gpt-4o",
        max_tokens=1000,
        messages=all_messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
```

Also confirm that all other service files import from `openai_client`, not `claude_client`:

```bash
# Check for any leftover references to claude_client
grep -r "claude_client" backend/services/
# Should return nothing. If it does, update those imports.
```

---

### Step 7 — Confirm the static frontend file exists

```bash
ls backend/static/
# Expected output: index.html
```

If `index.html` is missing, take the `catalyst.html` file, rename it to `index.html`, and move it into `backend/static/`.

---

### Step 8 — Run the development server

```bash
# Make sure you are inside backend/
cd backend

uvicorn main:app --reload --port 8000
```

Expected output:

```
INFO:     Will watch for changes in these directories: ['.../catalyst/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Application startup complete.
```

If you see any errors here, check [Common Errors & Fixes](#-common-errors--fixes) below.

---

### Step 9 — Open in browser

**Frontend (full UI):**
```
http://localhost:8000
```

**API docs (Swagger UI — test endpoints directly):**
```
http://localhost:8000/docs
```

The `/docs` page is especially useful during development. You can call each endpoint manually, inspect request/response shapes, and debug issues without touching the frontend.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key from platform.openai.com |

That is the only variable needed. No database, no Redis, no external queue. All session state is held in memory while the server runs.

---

## ▶️ Running the App

### Development (auto-reload on every file save)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Production (no reload, multiple workers)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

> ⚠️ With `--workers 2` or more, each worker has its own memory so sessions are not shared between workers. For true multi-worker production, replace the in-memory `sessions` dict in `routers/parse.py` with Redis.

### Manual API testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Parse JD + resume (plain text)
curl -X POST http://localhost:8000/api/parse/ \
  -F "jd_text=We need a Python backend engineer with FastAPI, PostgreSQL, Redis" \
  -F "resume_text=5 years Python. Built REST APIs with Flask. Some SQL experience."

# Parse with PDF upload
curl -X POST http://localhost:8000/api/parse/ \
  -F "jd_text=We need a Python backend engineer with FastAPI" \
  -F "resume_file=@/path/to/resume.pdf"

# Start skill assessment
curl -X POST http://localhost:8000/api/assess/start \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id-here"}'

# Send candidate answer
curl -X POST http://localhost:8000/api/assess/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id-here", "user_message": "I used FastAPI to build REST APIs for 2 years"}'

# Get gap analysis (after all skills assessed)
curl http://localhost:8000/api/gaps/your-session-id-here

# Generate learning plan
curl -X POST http://localhost:8000/api/plan/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id-here", "prioritised_gaps": []}'
```

---

## 📡 API Reference

### `POST /api/parse/`
Parses the JD and resume, extracts skills, and creates a new assessment session.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `jd_text` | string | ✅ Always | Full job description text |
| `resume_file` | file (PDF) | One of these two | Resume uploaded as PDF |
| `resume_text` | string | One of these two | Resume pasted as plain text |

**Response:**
```json
{
  "session_id": "3f8a1b2c-...",
  "required_skills": [
    { "name": "FastAPI", "category": "technical", "importance": 5 }
  ],
  "claimed_skills": [
    { "name": "Flask", "level": "5 years", "evidence": "Built REST APIs with Flask" }
  ],
  "gaps": [
    { "skill": "FastAPI", "status": "partial", "required_importance": 5, "claimed_level": "familiar" }
  ],
  "skills_to_assess": ["FastAPI", "PostgreSQL", "Redis"]
}
```

`status` is one of `matched`, `partial`, or `missing`. Only `partial` and `missing` skills enter the conversational assessment.

---

### `POST /api/assess/start`
Starts the assessment for the next pending skill and returns the opening question.

**Request:**
```json
{ "session_id": "3f8a1b2c-..." }
```

**Response:**
```json
{
  "skill": "FastAPI",
  "turn": 1,
  "message": "Walk me through a real project where you used FastAPI — what were you building?",
  "done": false
}
```

When `done` is `true`, all skills are assessed and you can call `/api/gaps/`.

---

### `POST /api/assess/message`
Sends the candidate's answer and returns either the next follow-up question or the final score for that skill.

**Request:**
```json
{
  "session_id": "3f8a1b2c-...",
  "user_message": "I built a REST API for an e-commerce platform..."
}
```

**Response — mid assessment:**
```json
{
  "message": "How did you handle authentication in that project?",
  "skill_complete": false,
  "turn": 2
}
```

**Response — skill complete:**
```json
{
  "message": "Thank you, that covers what I needed for this skill.",
  "skill_complete": true,
  "score": {
    "skill": "FastAPI",
    "score": 7.5,
    "conceptual_depth": 8.0,
    "practical_application": 7.0,
    "recency": 7.5,
    "rationale": "Solid hands-on experience. Good understanding of routing and dependency injection. Weaker on advanced features like background tasks."
  },
  "all_complete": false
}
```

When `all_complete` is `true`, proceed to `/api/gaps/`.

---

### `GET /api/gaps/{session_id}`
Returns the ranked gap analysis after all skills are assessed.

**Response:**
```json
{
  "ranked_gaps": [
    {
      "skill": "Kubernetes",
      "gap_score": 85,
      "adjacent_skills": ["Docker"],
      "adjacency_reason": "Candidate already knows Docker, covering ~40% of foundational Kubernetes concepts.",
      "estimated_weeks": 6
    }
  ]
}
```

`gap_score` = `required_importance × (10 − proficiency_score)`. Higher score = more urgent gap.

---

### `POST /api/plan/`
Generates the personalised 3-stage learning plan for the top gap skills.

**Request:**
```json
{
  "session_id": "3f8a1b2c-...",
  "prioritised_gaps": [ ]
}
```

Pass the `ranked_gaps` array from `/api/gaps/` as `prioritised_gaps`. Top 5 are used.

**Response:**
```json
{
  "plans": [
    {
      "skill": "Kubernetes",
      "total_weeks": 8,
      "stages": [
        {
          "name": "Foundation",
          "goal": "Understand containers, pods, and basic cluster concepts",
          "estimated_weeks": 2,
          "milestone": "Can deploy a simple app using kubectl and understand pod lifecycle",
          "resources": [
            {
              "title": "Kubernetes Official Interactive Tutorial",
              "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
              "type": "docs",
              "duration": "3 hours",
              "free": true
            }
          ]
        }
      ]
    }
  ]
}
```

---

### `GET /health`
Confirms the server is running.

**Response:**
```json
{ "status": "ok", "service": "catalyst" }
```

---

## 🐛 Common Errors & Fixes

### `ModuleNotFoundError: No module named 'routers'`
**Cause:** Server started from the repo root instead of `backend/`.

**Fix:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

---

### `FileNotFoundError: static/index.html not found`
**Cause:** `main.py` resolves `static/` relative to the working directory, not the file's location.

**Fix:** Ensure `main.py` uses an absolute path:
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
```

---

### `422 Unprocessable Entity` on `/api/parse/`
**Cause:** Sending the request as JSON instead of `multipart/form-data`.

**Fix:** The parse endpoint only accepts form data. Use `-F` flags in curl, not `-d`. The frontend handles this automatically.

---

### `openai.AuthenticationError: Incorrect API key provided`
**Cause:** `OPENAI_API_KEY` in `.env` is missing, misspelled, or invalid.

**Fix:**
1. Confirm `.env` is inside `backend/` (not the repo root)
2. Confirm the key starts with `sk-`
3. Confirm there are no quotes or extra spaces around the value
4. Check [platform.openai.com/api-keys](https://platform.openai.com/api-keys) to verify it is still active

---

### `openai.RateLimitError: You exceeded your current quota`
**Cause:** OpenAI account is out of credits.

**Fix:** Add credits at [platform.openai.com/settings/billing](https://platform.openai.com/settings/billing). $5 is enough for extensive hackathon testing.

---

### Assessment chat never ends — stuck after 6+ messages
**Cause:** GPT-4o did not trigger the `[ASSESSMENT_COMPLETE]` tag within the expected turns.

**Fix:** Add a hard turn cap of 6 in `routers/assess.py`:
```python
if skill_state.turns >= 6:
    score = force_score(skill_state.skill, skill_state.conversation)
    # mark skill as done and move on
```

---

### `ImportError: cannot import name 'openai_client'`
**Cause:** Service files still reference the old `claude_client` module.

**Fix:** Find and update all stale imports:
```bash
# Find all files that reference claude_client
grep -r "claude_client" backend/services/
```
Update each one from:
```python
from services.claude_client import chat
```
to:
```python
from services.openai_client import chat
```

---

### `CORS error` in browser console
**Cause:** Backend is not running, or the frontend is calling a different port.

**Fix:**
1. Confirm the backend is up (`uvicorn` shows `Application startup complete`)
2. The frontend uses `const API = '/api'` which is relative — since the HTML is served from the same FastAPI server, there should never be a CORS issue in local development

---

## 🤝 Contributing

This project was built for a hackathon. Ideas for extending it:

- **Replace in-memory sessions** with Redis for multi-worker production support
- **Add authentication** so candidates can resume interrupted assessments
- **Stream GPT responses** using SSE for a real-time typing effect in the chat UI
- **Recruiter dashboard** to compare proficiency scores across multiple candidates side by side
- **Export to PDF** using `weasyprint` so candidates receive a downloadable learning plan
- **Email delivery** to send the full report to the candidate after assessment

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">
  <strong>Built with GPT-4o · FastAPI · ❤️</strong><br/>
  <sub>Catalyst — Know beyond the resume.</sub>
</div>