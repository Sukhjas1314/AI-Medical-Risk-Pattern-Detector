Risk_Weights = {
    "Delayed Treatment": 40,
    "Missing Follow-up Diagonsis": 60
}

def calculate_risk_score(violations):
    """
    violations: list of rule violation dicts
    returns: (risk_score,risk_level)
    """

    score = 0
    explainations = []

    for v in violations: 
        rule = v["rule"]
        weight = Risk_Weights.get(rule,20)
        score += weight

        if "delay_hours" in v:
            explainations.append(
                f"{rule} Delay of {v['delay_hours']} hours (threshold {v['threshold']} hrs)"
            )
        else:
            explainations.append(f"{rule}: Required action missing")

    score = min(score,100)

    if score == 0:
        level = "LOW"
    elif score < 50:
        level = "MEDIUM"
    else: 
        level = "HIGH"

    return score,level,explainations