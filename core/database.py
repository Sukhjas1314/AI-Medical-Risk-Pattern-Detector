import sqlite3

def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        event_type TEXT,
        event_name TEXT,
        status TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_event(patient_id,event_type,event_name,status,timestamp):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events (patient_id,event_type,event_name,status,timestamp)
    VALUES (?, ?, ?, ?, ?)
    """,(patient_id,event_type,event_name,status,timestamp))

    conn.commit()
    conn.close()

def get_patient_events(patient_id):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT patient_id, event_type, event_name, status, timestamp
    FROM events
    WHERE patient_id = ?
    ORDER BY timestamp
    """,(patient_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "patient_id": r[0],
            "event_type": r[1],
            "event_name": r[2],
            "status": r[3],
            "timestamp": r[4]
        }
        for r in rows
    ]
