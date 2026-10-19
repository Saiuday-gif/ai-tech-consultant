import re

def extract_requirements(transcript_text):
    requirements = []
    lines = transcript_text.split("\n")
    
    for line in lines:
        line_clean = line.strip()
        lower = line_clean.lower()
        if not lower.startswith("client:"):
            continue
            
        if "logo" in lower or "branding" in lower:
            requirements.append({
                "feature": "Website Logo & Branding Configuration",
                "raw_text": line_clean,
                "category": "Branding",
                "default_hours": 3
            })
        if "stripe" in lower or "payment" in lower:
            requirements.append({
                "feature": "Stripe Payment Gateway Integration",
                "raw_text": line_clean,
                "category": "Finance",
                "default_hours": 5
            })
        if "search" in lower or "filter" in lower:
            requirements.append({
                "feature": "Member Search & Location Filters",
                "raw_text": line_clean,
                "category": "Directory Design",
                "default_hours": 6
            })
        if "csv" in lower or "import" in lower:
            requirements.append({
                "feature": "CSV Batch Member Import",
                "raw_text": line_clean,
                "category": "Data Migration",
                "default_hours": 8
            })
        if "video" in lower or "webrtc" in lower or "consultation" in lower:
            requirements.append({
                "feature": "Custom Real-time Video Consultation Module",
                "raw_text": line_clean,
                "category": "Custom Engineering",
                "default_hours": 35
            })
            
    seen = set()
    deduped = []
    for req in requirements:
        if req["feature"] not in seen:
            seen.add(req["feature"])
            deduped.append(req)
            
    return deduped