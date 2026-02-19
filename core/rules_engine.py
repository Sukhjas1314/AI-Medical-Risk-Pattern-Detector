from datetime import datetime


Care_Rules = {
    "abnormal_test_followup": 24,
    "diagnosis_to_treatment": 12
}


def hours_between(t1,t2):
    fmt = "%Y-%m-%d %H:%M"
    return abs((datetime.strptime(t2,fmt) - datetime.strptime(t1,fmt)).total_seconds())/3600


def check_care_rules(timeline):
    """
    timeline: list of events sorted by timelstamp
    returns: list of rule violations
    """

    violations = []

    last_abnormal_test_time = None
    diagnosis_time = None

    for event in timeline:
        if event['event_type'] == "lab_test_result" and event["status"] == "abnormal":
            last_abnormal_test_time = event["timestamp"]

        if event["event_type"] == "diagnosis":
            diagnosis_time = event["timestamp"]

        if event["event_type"] == "treatment" and diagnosis_time:
            delay = hours_between(diagnosis_time,event["timestamp"])
            if delay > Care_Rules["diagnosis_to_treatment"]:
                violations.append({
                    "rule": "Delayed Treatment",
                    "delay_hours": round(delay,2),
                    "threshold": Care_Rules["diagnosis_to_treatment"]
                })

    if last_abnormal_test_time and not diagnosis_time:
        violations.append({
            "rule": "Missing Follow-up Diagnosis",
            "details": "Abnormal test not followed by diagnosis"
        })
    
    return violations