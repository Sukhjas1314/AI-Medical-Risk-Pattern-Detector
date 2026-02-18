from fastapi import FastAPI
import json

from core.rules_engine import check_care_rules
from core.risk_scoring import calculate_risk_score
from core.explainability import generate_explainations
from core.timeline_builder import build_timeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "AI Medical Risk Pattern Detector")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Medical Risk Detection API is running."}

@app.post("/analyze_patient")
def analyze_patient(patient_id: str):
    try: 
        with open("data/patients.json") as f:
            data = json.load(f)
    except Exception:
        return {"error": "Unable to load patient dataset."}

    if not patient_id:
        return {"error": "Patient ID is required."}

    # Filter patient timeline
    timeline = [e for e in data if e["patient_id"] == patient_id]
    timeline.sort(key = lambda x: x["timestamp"])

    if not timeline:
        return {"error": f"No data found for patient ID {patient_id}"}

    violations = check_care_rules(timeline)
    score, level, _ = calculate_risk_score(violations)
    explainations = generate_explainations(violations)
    timeline_view = build_timeline(timeline, violations)


    return {
        "patient_id": patient_id,
        "risk_score": score,
        "risk_level": level,
        "violations": violations,
        "explainations": explainations,
        "timeline": timeline_view
    }