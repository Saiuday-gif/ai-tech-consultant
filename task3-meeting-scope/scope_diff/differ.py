def compare_scopes(scope_v1, scope_v2):
    features_v1 = {item["feature"]: item for item in scope_v1.get("line_items", [])}
    features_v2 = {item["feature"]: item for item in scope_v2.get("line_items", [])}

    added = []
    removed = []
    retained = []

    for feat, data in features_v2.items():
        if feat not in features_v1:
            added.append(data)
        else:
            retained.append({
                "feature": feat,
                "original_hours": features_v1[feat]["hours"],
                "new_hours": data["hours"],
                "hours_delta": data["hours"] - features_v1[feat]["hours"]
            })

    for feat, data in features_v1.items():
        if feat not in features_v2:
            removed.append(data)

    hours_delta = scope_v2["total_estimated_hours"] - scope_v1["total_estimated_hours"]
    cost_delta = scope_v2["total_estimated_cost"] - scope_v1["total_estimated_cost"]

    return {
        "summary": {
            "v1_total_hours": scope_v1["total_estimated_hours"],
            "v2_total_hours": scope_v2["total_estimated_hours"],
            "hours_difference": hours_delta,
            "cost_difference": cost_delta
        },
        "added_features": added,
        "removed_features": removed,
        "retained_features": retained
    }