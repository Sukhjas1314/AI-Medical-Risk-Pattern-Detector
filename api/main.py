from fastapi import FastAPI
import json

from core.rules_engine import check_care_rules
from core.risk_scoring import calculate_risk_score
from core.explainability import generate_explainations
from core.timeline_builder import build_timeline
from fastapi.middleware.cors import CORSMiddleware
from core.anomaly_detector import extract_features, detect_anomaly
from core.database import init_db, get_patient_events
from core.database import insert_event
from fastapi_utils.tasks import repeat_every
import time

init_db()



app = FastAPI(title = "AI Medical Risk Pattern Detector")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
@repeat_every(seconds=60)
def monitor_patients():
    print("Running real-time monitoring...")
    # In real system: loop through active patients and evaluate risk


@app.get("/")
def home():
    return {"message": "AI Medical Risk Detection API is running."}

@app.post("/add_event")
def add_event(patient_id: str,
              event_type: str,
              event_name: str,
              status: str,
              timestamp: str):

    insert_event(patient_id, event_type, event_name, status, timestamp)

    return {"message": "Event added successfully"}

@app.post("/analyze_patient")
def analyze_patient(patient_id: str):
    # try: 
    #     with open("data/patients.json") as f:
    #         data = json.load(f)
    # except Exception:
    #     return {"error": "Unable to load patient dataset."}

    # if not patient_id:
    #     return {"error": "Patient ID is required."}

    if not patient_id:
        return {"error": "Patient ID is required."}

    # Fetch events from database instead of JSON
    timeline = get_patient_events(patient_id)

    # Filter patient timeline
    # timeline = [e for e in data if e["patient_id"] == patient_id]
    timeline.sort(key = lambda x: x["timestamp"])

    if not timeline:
        return {"error": f"No data found for patient ID {patient_id}"}

    violations = check_care_rules(timeline)
    score, level, _ = calculate_risk_score(violations)
    explainations = generate_explainations(violations)
    timeline_view = build_timeline(timeline, violations)

    features = extract_features(timeline, violations)
    is_anomalous, anomaly_score = detect_anomaly(features)

    return {
        "patient_id": patient_id,
        "risk_score": score,
        "risk_level": level,
        "violations": violations,
        "explainations": explainations,
        "timeline": timeline_view,
        "anomaly_detected": is_anomalous,
        "anomaly_score": anomaly_score
    }

