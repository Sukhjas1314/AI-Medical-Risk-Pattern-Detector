async function analyze() {
    const patientId = document.getElementById("patientId").value;
    if (!patientId.trim()) {
        alert("Please enter a Patient ID.");
        return;
    }

    const response = await fetch(
        `http://127.0.0.1:8000/analyze_patient?patient_id=${patientId}`,
        { method: "POST" }
    );

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById("results").style.display = "block";
    document.getElementById("score").innerText = data.risk_score;

    const levelSpan = document.getElementById("level");
    levelSpan.innerText = data.risk_level;
    levelSpan.className = "risk-badge " + data.risk_level.toLowerCase();

    const explainationsList = document.getElementById("explainations");
    explainationsList.innerHTML = "";

    if (data.explainations.length === 0) {
        explainationsList.innerHTML = "<li>No risk detected. Care protocol followed correctly.</li>";
    }
    else{
        data.explainations.forEach(e => {
            const li = document.createElement("li");
            li.innerText = e;
            explainationsList.appendChild(li);
        });
    }

    const timelineDiv = document.getElementById("timeline");
    timelineDiv.innerHTML = "";

    data.timeline.forEach(t => {
        const div = document.createElement("div");
        div.className = "timeline-item";
        if (t.risk_flag) {
            div.className += " timeline-risk";
        }
        div.innerHTML = `<strong>${t.time}</strong> - ${t.label} (${t.status})`;
        timelineDiv.appendChild(div);
    });

    document.getElementById("anomalyScore").innerText = data.anomaly_score;
    document.getElementById("anomalyFlag").innerText = data.anomaly_detected ? "Yes" : "No";
}