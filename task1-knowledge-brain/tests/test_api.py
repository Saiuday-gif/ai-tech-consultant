import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ingestion():
    response = client.post("/ingestion/run?limit=3")
    assert response.status_code == 200
    assert "processed_articles" in response.json()

def test_query_success():
    response = client.post("/query", json={"question": "How to update logo"})
    assert response.status_code == 200
    assert response.json()["status"] == "answered"
    assert len(response.json()["sources"]) > 0

def test_query_insufficient_evidence():
    response = client.post("/query", json={"question": "xyz completely unknown question abc"})
    assert response.status_code == 200
    assert response.json()["status"] == "insufficient_evidence"
    assert response.json()["needs_human"] is True

def test_escalations_list():
    response = client.get("/escalations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)