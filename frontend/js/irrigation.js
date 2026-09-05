requireAuth();

const SCHEDULE_KEY = "sa_irrigation_schedules";
let currentStatus = "OFF";

function loadSchedules() {
  try { return JSON.parse(localStorage.getItem(SCHEDULE_KEY)) || []; }
  catch (_) { return []; }
}

function saveSchedules(schedules) {
  localStorage.setItem(SCHEDULE_KEY, JSON.stringify(schedules));
}

function renderSchedules() {
  const schedules = loadSchedules();
  const list = document.getElementById("scheduleList");

  if (!schedules.length) {
    list.innerHTML = `<div class="state-box"><span class="state-icon">🗓️</span>No irrigation schedules yet. Add one above.</div>`;
    return;
  }

  list.innerHTML = schedules.map((s, i) => `
    <div class="alert-item">
      <div class="alert-dot info"></div>
      <div style="flex:1;">
        <div class="alert-text"><strong>${s.crop}</strong> — ${s.date} at ${s.time} for ${s.duration} minutes</div>
      </div>
      <button class="btn btn-secondary" style="padding:6px 12px; font-size:0.8rem;" data-remove-index="${i}">Remove</button>
    </div>
  `).join("");

  list.querySelectorAll("[data-remove-index]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const idx = parseInt(btn.getAttribute("data-remove-index"), 10);
      const updated = loadSchedules();
      updated.splice(idx, 1);
      saveSchedules(updated);
      renderSchedules();
    });
  });
}

document.getElementById("scheduleForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const schedules = loadSchedules();
  schedules.push({
    date: document.getElementById("schedDate").value,
    time: document.getElementById("schedTime").value,
    duration: document.getElementById("schedDuration").value,
    crop: document.getElementById("schedCrop").value,
  });
  saveSchedules(schedules);
  renderSchedules();
  e.target.reset();
  document.getElementById("schedDuration").value = 15;
});

function setStatusPill(status) {
  currentStatus = status;
  const on = status === "ON";
  document.getElementById("valIrrigationStatus").innerHTML = on
    ? `<span class="pill pill-info">💧 IRRIGATION ON</span>`
    : `<span class="pill pill-neutral">IRRIGATION OFF</span>`;
}

async function loadIrrigation() {
  document.getElementById("loadingState").style.display = "flex";
  document.getElementById("irrigationContent").style.display = "none";
  document.getElementById("errorState").style.display = "none";

  const [sensorsRes, statusRes] = await Promise.all([getSensors(), getIrrigationStatus()]);

  if (!sensorsRes.ok && !statusRes.ok) {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "flex";
    document.getElementById("errorMessage").textContent = friendlyErrorMessage(statusRes);
    return;
  }

  if (sensorsRes.ok && sensorsRes.data) {
    const s = sensorsRes.data;
    document.getElementById("valMoisture").innerHTML = `${s.soil_moisture} <span class="unit">%</span>`;
    document.getElementById("valWaterLevel").innerHTML = `${s.water_level} <span class="unit">%</span>`;
    document.getElementById("valTemperature").innerHTML = `${s.temperature} <span class="unit">°C</span>`;
    document.getElementById("valHumidity").innerHTML = `${s.humidity} <span class="unit">%</span>`;
    document.getElementById("valRainPrediction").innerHTML = `${s.rain_prediction_pct} <span class="unit">%</span>`;
  }

  if (statusRes.ok && statusRes.data) {
    setStatusPill(statusRes.data.status);
    document.getElementById("recommendationText").textContent = statusRes.data.recommendation;
  }

  renderSchedules();

  document.getElementById("loadingState").style.display = "none";
  document.getElementById("irrigationContent").style.display = "block";
}

/* ---------------------------------------------------------
   Manual controls
   --------------------------------------------------------- */
const autoToggle = document.getElementById("autoIrrigationToggle");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const controlHint = document.getElementById("controlHint");

function updateControlAvailability() {
  const autoOn = autoToggle.checked;
  startBtn.disabled = autoOn;
  stopBtn.disabled = autoOn;
  controlHint.textContent = autoOn
    ? "Auto irrigation is ON — manual Start/Stop is disabled. Turn it off to control irrigation manually."
    : "Auto irrigation is OFF — use Start/Stop to control irrigation manually.";
}

autoToggle.addEventListener("change", () => {
  localStorage.setItem("sa_auto_irrigation", autoToggle.checked ? "true" : "false");
  updateControlAvailability();
});

startBtn.addEventListener("click", async () => {
  startBtn.disabled = true;
  const result = await startIrrigation();
  startBtn.disabled = false;
  if (result.ok) setStatusPill("ON");
});

stopBtn.addEventListener("click", async () => {
  stopBtn.disabled = true;
  const result = await stopIrrigation();
  stopBtn.disabled = false;
  if (result.ok) setStatusPill("OFF");
});

// Restore auto-irrigation toggle preference
autoToggle.checked = localStorage.getItem("sa_auto_irrigation") === "true";
updateControlAvailability();

document.addEventListener("DOMContentLoaded", loadIrrigation);
