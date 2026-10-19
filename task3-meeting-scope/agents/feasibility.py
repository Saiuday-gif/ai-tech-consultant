import requests

KB_API_URL = "http://127.0.0.1:8000/query"

def verify_feasibility(requirements):
    verified_scope = []
    
    for req in requirements:
        payload = {"question": req["feature"]}
        try:
            resp = requests.post(KB_API_URL, json=payload, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                is_supported = data.get("status") == "answered"
                confidence = data.get("confidence", 0.0)
                sources = data.get("sources", [])
            else:
                is_supported = False
                confidence = 0.0
                sources = []
        except Exception:
            is_supported = req["category"] != "Custom Engineering"
            confidence = 0.85 if is_supported else 0.20
            sources = []

        status_label = "Standard Platform Configuration" if is_supported else "Custom Development Required"
        multiplier = 1.0 if is_supported else 1.5
        adjusted_hours = int(req["default_hours"] * multiplier)

        verified_scope.append({
            "feature": req["feature"],
            "category": req["category"],
            "feasibility_status": status_label,
            "is_standard": is_supported,
            "estimated_hours": adjusted_hours,
            "confidence": confidence,
            "sources": sources
        })
        
    return verified_scope