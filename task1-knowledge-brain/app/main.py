import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from ingestion.crawler import run_ingestion
from retrieval.vector_store import index_articles, search_knowledge
from multimodal.vision import process_image_context

app = FastAPI(title="Knowledge Brain API")

ESCALATIONS = []

class QueryRequest(BaseModel):
    question: str

class SourceItem(BaseModel):
    title: str
    url: str
    image_url: Optional[str] = ""

class QueryResponse(BaseModel):
    answer: str
    status: str
    sources: List[SourceItem]
    confidence: float
    needs_human: bool

class EscalationResolveRequest(BaseModel):
    approved_answer: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "Knowledge Brain"}

@app.post("/ingestion/run")
def trigger_ingest(limit: int = 10):
    docs = run_ingestion(limit=limit)
    if docs:
        for doc in docs:
            doc["images"] = process_image_context(doc.get("images", []))
        index_articles(docs)
    return {"status": "completed", "processed_articles": len(docs)}

@app.post("/query", response_model=QueryResponse)
def query_knowledge(req: QueryRequest):
    evidence = search_knowledge(req.question, n_results=2)
    
    if not evidence:
        ESCALATIONS.append({"question": req.question, "status": "pending"})
        return QueryResponse(
            answer="This request requires specialized human verification as the knowledge base is inconclusive.",
            status="insufficient_evidence",
            sources=[],
            confidence=0.1,
            needs_human=True
        )

    top_item = evidence[0]
    generated_answer = f"According to '{top_item['title']}': {top_item['content']}"

    sources = [
        SourceItem(title=e["title"], url=e["url"], image_url=e["image_url"])
        for e in evidence
    ]

    return QueryResponse(
        answer=generated_answer,
        status="answered",
        sources=sources,
        confidence=0.92,
        needs_human=False
    )

@app.get("/escalations")
def get_escalations():
    return ESCALATIONS

@app.post("/escalations/{item_id}/resolve")
def resolve_escalation(item_id: int, req: EscalationResolveRequest):
    if item_id >= len(ESCALATIONS):
        raise HTTPException(status_code=404, detail="Escalation ID not found")
    ESCALATIONS[item_id]["resolved_answer"] = req.approved_answer
    ESCALATIONS[item_id]["status"] = "resolved"
    return {"message": "Escalation resolved successfully"}