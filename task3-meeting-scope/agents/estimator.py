HOURLY_RATE = 85

def generate_scope_proposal(verified_scope, project_title="Client Project Scope"):
    total_hours = sum(item["estimated_hours"] for item in verified_scope)
    total_cost = total_hours * HOURLY_RATE
    
    proposal = {
        "project_title": project_title,
        "hourly_rate": HOURLY_RATE,
        "total_estimated_hours": total_hours,
        "total_estimated_cost": total_cost,
        "line_items": []
    }
    
    for idx, item in enumerate(verified_scope, start=1):
        cost = item["estimated_hours"] * HOURLY_RATE
        proposal["line_items"].append({
            "item_number": idx,
            "feature": item["feature"],
            "category": item["category"],
            "classification": item["feasibility_status"],
            "hours": item["estimated_hours"],
            "subtotal": cost
        })
        
    return proposal