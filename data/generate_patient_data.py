import random
from datetime import datetime, timedelta
import json

Event_Types = [
    "lab_test_result",
    "diagnosis",
    "treatment",
    "follow_up"
]

def generate_timestamp(start_time,hours_offset):
    return (start_time + timedelta(hours = hours_offset)).strftime("%Y-%m-%d %H:%M")

def generate_patient(patient_id,risky = False):
    start_time = datetime(2026,2,6,10,0)
    events = []

    status = "abnormal" if risky else "normal"
    events.append({
        "patient_id": patient_id,
        "event_type": "lab_test_result",
        "event_name": "Blood Sugar",
        "status": status,
        "timestamp": generate_timestamp(start_time,1),
        "notes": "Generate test result"
    })

    events.append({
        "patient_id": patient_id,
        "event_type": "diagnosis",
        "event_name": "Diabetes",
        "status": "confirmed",
        "timestamp": generate_timestamp(start_time,4),
        "notes": "Diagnosis recorded"
    })

    treatment_delay = 30 if risky else 8
    events.append({
        "patient_id": patient_id,
        "event_type": "treatment",
        "event_name": "Insulin Therapy",
        "status": "started",
        "timestamp": generate_timestamp(start_time,treatment_delay),
        "notes": "Treatment initiated"
    })

    return events


def generate_dataset(num_patients = 50):
    dataset = []
    for i in range(num_patients):
        risky = random.choice([True,False])
        dataset.extend(generate_patient(f"P{i+1:03}",risky))

    return dataset

if __name__ == "__main__":
    data = generate_dataset()
    with open("patients.json","w") as f:
        json.dump(data,f,indent = 2)
    print("Synthetic patient data generated : patients.json")