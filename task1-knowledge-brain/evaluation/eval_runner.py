import requests
import json

BASE_URL = "http://127.0.0.1:8000"

TEST_CASES = [
    {"question": "How do I upload or update my website logo?", "expected_status": "answered"},
    {"question": "How to configure Stripe payment gateway credentials?", "expected_status": "answered"},
    {"question": "How to edit member search results design and filters?", "expected_status": "answered"},
    {"question": "What is the procedure for launching a space rocket?", "expected_status": "insufficient_evidence"},
    {"question": "Where do I find Brand Info in admin?", "expected_status": "answered"},
    {"question": "How to set mode to Live in payments?", "expected_status": "answered"},
    {"question": "Can I filter members by location?", "expected_status": "answered"},
    {"question": "How do I book an international flight ticket?", "expected_status": "insufficient_evidence"},
    {"question": "Where is General Settings located?", "expected_status": "answered"},
    {"question": "What API keys are required for Stripe?", "expected_status": "answered"},
    {"question": "How to enable category filter in search?", "expected_status": "answered"},
    {"question": "What is the company stock price today?", "expected_status": "insufficient_evidence"},
    {"question": "How to upload PNG images for branding?", "expected_status": "answered"},
    {"question": "Where is Finance menu in dashboard?", "expected_status": "answered"},
    {"question": "Can I search members by keyword?", "expected_status": "answered"},
    {"question": "What is the recipe for chocolate cake?", "expected_status": "insufficient_evidence"},
    {"question": "How do I save changes after uploading logo?", "expected_status": "answered"},
    {"question": "Where do I enter publishable key for payment?", "expected_status": "answered"},
    {"question": "How to access Member Search settings?", "expected_status": "answered"},
    {"question": "Who won the cricket match yesterday?", "expected_status": "insufficient_evidence"}
]

def run_evaluations():
    passed = 0
    total = len(TEST_CASES)
    results = []

    for idx, test in enumerate(TEST_CASES, start=1):
        try:
            resp = requests.post(f"{BASE_URL}/query", json={"question": test["question"]}, timeout=5)
            data = resp.json()
            is_pass = data.get("status") == test["expected_status"]
            if is_pass:
                passed += 1
            results.append({
                "case_id": f"KB-{idx:03d}",
                "question": test["question"],
                "expected": test["expected_status"],
                "actual": data.get("status"),
                "passed": is_pass
            })
        except Exception as e:
            results.append({
                "case_id": f"KB-{idx:03d}",
                "question": test["question"],
                "error": str(e),
                "passed": False
            })

    print(json.dumps({"total": total, "passed": passed, "accuracy": f"{(passed/total)*100:.1f}%"}, indent=2))
    return results

if __name__ == "__main__":
    run_evaluations()