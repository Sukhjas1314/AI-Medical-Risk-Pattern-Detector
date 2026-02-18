import numpy as np
from sklearn.ensemble import IsolationForest

def extract_features(timeline,violations):
    """
    Convert patient timeline into numeric feature vector
    """

    total_events = len(timeline)
    num_violations = len(violations)

    # Calculate total delay hours
    total_delay = 0
    for v in violations:
        if "delay_hours" in v:
            total_delay += v["delay_hours"]

    return [total_events,num_violations,total_delay]


def detect_anomaly(feature_vector):
    """
    Run Isolation Forest on single patient feature vector
    """

    # For demo puposes, create synthetic baseline
    baseline_data = np.array([
        [4,0,0],
        [4,0,2],
        [4,1,5],
        [4,0,1],
        [4,1,3]
    ])

    model = IsolationForest(contamination = 0.2,random_state = 42)
    model.fit(baseline_data)

    predicion = model.predict([feature_vector])
    score = model.decision_function([feature_vector])[0]

    is_anomalous = True if predicion[0] == -1 else False

    return is_anomalous, round(float(score),3)