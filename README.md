# AI Tech Consultant Platform

End-to-end technical consulting platform comprising a Knowledge Brain, automated Inbox Agent with autonomy tracking, and an automated Meeting-to-Scope proposal generator.

## Project Structure
- task1-knowledge-brain/: Python/FastAPI knowledge retrieval service with multimodal grounding.
- task2-inbox-agent/: Node.js/TypeScript email classification and draft generation engine.
- task3-meeting-to-scope/: Multi-agent meeting transcript analysis and scope diff engine.
- shared-docs/: Shared schemas and cross-service contracts.

## Quick Start Instructions

### 1. Task 1: Knowledge Brain
```bash
cd task1-knowledge-brain
uvicorn app.main:app --reload --port 8000 

### 2. Task 2: Inbox Agent (Node.js)
Triage, classification, draft generation, and human review autonomy tracking.

```bash
cd task2-inbox-agent
npm install
node src/index.js 

### 3. Task 3: Meeting-to-Scope Engine (FastAPI)
Transcript feature extraction, feasibility checks against Knowledge Brain, and Scope Diff comparison service on port 8001.

```bash
cd task3-meeting-to-scope
python -m venv venv
# Windows activate:
venv\Scripts\activate
# Linux/Mac activate:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
API Documentation & Swagger UI: http://127.0.0.1:8001/docs

Run Unit Tests: pytest tests/

Run Evaluation Runner: python src/evaluation/eval_runner.py

## Architecture & Documentation

Comprehensive architectural design, benchmark analyses, and development logs are documented in:
- `DESIGN.md`: Cross-service architecture, schemas, and trade-off decisions.
- `EVALS.md`: 20-sample benchmark results (80% benchmark compliance) and failure mode analysis.
- `AI_LOG.md`: Detailed logs of AI-assisted scaffolding, test generation, and debugging.
- `shared-docs/api_contracts.md`: Interface contracts and data structures across services.

