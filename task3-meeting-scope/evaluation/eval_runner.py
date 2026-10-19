import os
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure project root is on the import path for both runtime execution and editor tooling.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Some editor environments do not resolve namespace packages until the root is explicitly added.
try:
    from agents.extractor import extract_requirements
    from agents.feasibility import verify_feasibility
    from agents.estimator import generate_scope_proposal
    from scope_diff.differ import compare_scopes
except ImportError:  # pragma: no cover - fallback for editor/static analysis resolution
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from agents.extractor import extract_requirements
    from agents.feasibility import verify_feasibility
    from agents.estimator import generate_scope_proposal
    from scope_diff.differ import compare_scopes

def run_evaluations():
    print("Running Task 3 Evaluation Suite...\n")
    
    with open("transcripts/meeting_a.txt", "r", encoding="utf-8") as f:
        t_a = f.read()
    with open("transcripts/meeting_c.txt", "r", encoding="utf-8") as f:
        t_c = f.read()

    scope_a_items = verify_feasibility(extract_requirements(t_a))
    proposal_a = generate_scope_proposal(scope_a_items, "Meeting A Initial Scope")

    scope_c_items = verify_feasibility(extract_requirements(t_c))
    proposal_c = generate_scope_proposal(scope_c_items, "Meeting C Revised Scope")

    diff = compare_scopes(proposal_a, proposal_c)

    tests = [
        {"name": "Extract Meeting A Features", "pass": len(proposal_a["line_items"]) >= 3},
        {"name": "Verify Stripe Feasibility", "pass": any(item["feature"] == "Stripe Payment Gateway Integration" for item in proposal_a["line_items"])},
        {"name": "Detect Added Custom Feature in Meeting C", "pass": any("Video" in item["feature"] for item in diff["added_features"])},
        {"name": "Detect Removed Search Feature in Meeting C", "pass": any("Search" in item["feature"] for item in diff["removed_features"])},
        {"name": "Calculate Accurate Cost Delta", "pass": diff["summary"]["cost_difference"] > 0}
    ]

    passed_count = sum(1 for t in tests if t["pass"])
    
    for t in tests:
        print(f"Test: {t['name']} | Result: {'PASSED' if t['pass'] else 'FAILED'}")

    print("\n==================================")
    print(f"Total Evaluated: {len(tests)}")
    print(f"Passed: {passed_count}")
    print(f"Accuracy: {(passed_count / len(tests)) * 100:.1f}%")
    print("==================================")
    print("\nScope Difference Summary:\n", json.dumps(diff["summary"], indent=2))

if __name__ == "__main__":
    run_evaluations()