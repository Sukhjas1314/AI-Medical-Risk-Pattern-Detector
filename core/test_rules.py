import json
from rules_engine import check_care_rules
from risk_scoring import calculate_risk_score
from explainability import generate_explainations
from timeline_builder import build_timeline

with open("data/patients.json") as f:
    data = json.load(f)

# Take one Patient
patient_id = data[0]["patient_id"]
timeline = [e for e in data if e["patient_id"] == patient_id]

# Sort by time
timeline.sort(key = lambda x: x["timestamp"])

violations = check_care_rules(timeline)
score,level,explaination = calculate_risk_score(violations)
detailed_explainations = generate_explainations(violations)
timeline_view = build_timeline(timeline, violations)

print("Violations : ",violations)
print("Risk score : ",score)
print("Risk Level : ",level)
print("\nExplainable Risk Narratives : ")
for e in detailed_explainations:
    print("-",e)

print("\nPatient Timeline View : ")
for t in timeline_view:
    flag = "⚠️" if t["risk_flag"] else "✓"
    print(f"{flag} {t['time']} - {t['label']} ({t['status']})")