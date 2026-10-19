import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from agents.extractor import extract_requirements
from agents.feasibility import verify_feasibility
from agents.estimator import generate_scope_proposal
from scope_diff.differ import compare_scopes

app = FastAPI(title="Meeting-to-Scope Engine API")

class TranscriptRequest(BaseModel):
    transcript_text: str
    project_title: str = "Client Implementation Scope"

class CompareRequest(BaseModel):
    scope_v1: Dict[str, Any]
    scope_v2: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "ok", "service": "Meeting-to-Scope Engine"}

@app.post("/scope/generate")
def create_scope_from_transcript(req: TranscriptRequest):
    reqs = extract_requirements(req.transcript_text)
    if not reqs:
        raise HTTPException(status_code=400, detail="No actionable project requirements identified.")
    verified = verify_feasibility(reqs)
    proposal = generate_scope_proposal(verified, req.project_title)
    return proposal

@app.post("/scope/compare")
def compare_meeting_scopes(req: CompareRequest):
    diff = compare_scopes(req.scope_v1, req.scope_v2)
    return diff