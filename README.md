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