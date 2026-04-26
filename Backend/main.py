from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from routers import parse, assess, gaps, plan
import os

load_dotenv()

app = FastAPI(title="Catalyst API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(parse.router, prefix="/api/parse", tags=["Parse"])
app.include_router(assess.router, prefix="/api/assess", tags=["Assess"])
app.include_router(gaps.router,   prefix="/api/gaps",   tags=["Gaps"])
app.include_router(plan.router,   prefix="/api/plan",   tags=["Plan"])

# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")