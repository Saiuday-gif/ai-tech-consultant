import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from agents.extractor import extract_requirements
from scope_diff.differ import compare_scopes

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("Test 1: Health Check -> PASSED")

def test_extract_requirements():
    sample_text = "Client: We need to upload our logo and configure Stripe payment."
    reqs = extract_requirements(sample_text)
    assert len(reqs) == 2
    features = [r["feature"] for r in reqs]
    assert "Website Logo & Branding Configuration" in features
    assert "Stripe Payment Gateway Integration" in features
    print("Test 2: Requirements Extraction -> PASSED")

def test_scope_generate_endpoint():
    payload = {
        "transcript_text": "Client: We want to upload our custom medical association logo.\nConsultant: Yes, sure.",
        "project_title": "Test Medical Portal"
    }
    response = client.post("/scope/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_title"] == "Test Medical Portal"
    assert len(data["line_items"]) >= 1
    assert data["total_estimated_hours"] > 0
    print("Test 3: Scope Generation API -> PASSED")

def test_scope_compare():
    scope_v1 = {
        "project_title": "V1",
        "hourly_rate": 85,
        "total_estimated_hours": 10,
        "total_estimated_cost": 850,
        "line_items": [{"feature": "Logo Setup", "hours": 10}]
    }
    scope_v2 = {
        "project_title": "V2",
        "hourly_rate": 85,
        "total_estimated_hours": 35,
        "total_estimated_cost": 2975,
        "line_items": [{"feature": "Logo Setup", "hours": 10}, {"feature": "Video Call", "hours": 25}]
    }
    diff = compare_scopes(scope_v1, scope_v2)
    assert len(diff["added_features"]) == 1
    assert diff["summary"]["hours_difference"] == 25
    print("Test 4: Scope Comparison Logic -> PASSED")

if __name__ == "__main__":
    print("Running Task 3 Unit Tests...\n")
    test_health()
    test_extract_requirements()
    test_scope_generate_endpoint()
    test_scope_compare()
    print("\n==================================")
    print("All Task 3 unit tests passed successfully (4/4 passed).")
    print("==================================")