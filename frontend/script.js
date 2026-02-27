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

    const alertBanner = document.getElementById("alertBanner");
    if (data.risk_level === "High"){
        alertBanner.style.display = "block";
        alertBanner.innerText = "⚠ HIGH RISK PATIENT — Immediate Attention Required";
    } else{
        alertBanner.style.display = "none";
    }

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

    const hasTreatment = data.timeline.some(t => t.label.includes("Treatment"));

    if (!hasTreatment && data.risk_level !== "LOW"){
        alertBanner.style.display = "block";
        alertBanner.innerText = "⏳ Pending Treatment — Risk Escalating"
    }

    document.getElementById("anomalyScore").innerText = data.anomaly_score;
    document.getElementById("anomalyFlag").innerText = data.anomaly_detected ? "Yes" : "No";
}

async function loadPatients(){
    const response = await fetch("http://127.0.0.1:8000/patients");
    const data = await response.json();

    const list = document.getElementById("patientList");
    list.innerHTML = "";

    data.patients.forEach(p => {
        const li = document.createElement("li");
        li.innerText = p;
        li.style.cursor = "pointer";
        li.onclick = () =>{
            document.getElementById("patientId").value = p;
            analyze();
        };
        list.appendChild(li);
    });
}

loadPatients();

setInterval(() => {
    loadPatients();
}, 10000);
