def build_timeline(events,violations):
    """
    events: list of patient events
    violations: detected rule violations
    returns: formatted timeline for visualization
    """
    risk_rules = {v["rule"] for v in violations}
    timeline = []

    for e in events:
        item = {
            "time": e["timestamp"],
            "label": f"{e['event_name']} ({e['event_type'].replace('_',' ').title()})",
            "status": e["status"],
            "risk_flag": False
        }    

        # Flag risky points
        if e["event_type"] == "treatment" and "Delayed Treatment" in risk_rules:
            item["risk_flag"] = True

        timeline.append(item)

    return timeline