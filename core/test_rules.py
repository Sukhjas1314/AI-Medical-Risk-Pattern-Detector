import json
from rules_engine import check_care_rules
from risk_scoring import calculate_risk_score

with open("data/patients.json") as f:
    data = json.load(f)

# Take one Patient
patient_id = data[0]["patient_id"]
timeline = [e for e in data if e["patient_id"] == patient_id]

# Sort by time
timeline.sort(key = lambda x: x["timestamp"])

violations = check_care_rules(timeline)
score,level,explainations = calculate_risk_score(violations)

print("Violations : ",violations)
print("Risk score : ",score)
print("Risk Level : ",level)
print("Explainations : ",explainations)
