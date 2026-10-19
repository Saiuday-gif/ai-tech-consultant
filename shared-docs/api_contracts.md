# Shared Architecture & API Contracts

## Services Interaction Map
1. Task 1 (Knowledge Brain - Port 8000): Serves verified documentation chunks, citations, and escalation records.
2. Task 2 (Inbox Agent - Node.js): Consumes POST http://127.0.0.1:8000/query to ground email drafts against documentation.
3. Task 3 (Meeting-to-Scope - Port 8001): Consumes POST http://127.0.0.1:8000/query to verify platform feasibility of extracted requirements.

## Core Data Schema
- Query Request: {"question": string}
- Query Response: {"answer": string, "status": string, "sources": array, "confidence": float, "needs_human": boolean}