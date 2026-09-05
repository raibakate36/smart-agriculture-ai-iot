requireAuth();

function fmtTime(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch (_) {
    return "--";
  }
}

function alertDotClass(level) {
  if (level === "red") return "red";
  if (level === "yellow") return "yellow";
  if (level === "green") return "green";
  return "info";
}

function riskPillClass(risk) {
  if (risk === "Low") return "pill-good";
  if (risk === "Moderate") return "pill-warn";
  if (risk === "High") return "pill-critical";
  return "pill-neutral";
}

async function loadDashboard() {
  document.getElementById("loadingState").style.display = "flex";
  document.getElementById("dashboardContent").style.display = "none";
  document.getElementById("errorState").style.display = "none";

  const [dashRes, weatherRes] = await Promise.all([getDashboardData(), getWeather()]);

  if (!dashRes.ok || !dashRes.data) {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "flex";
    document.getElementById("errorMessage").textContent = friendlyErrorMessage(dashRes);
    return;
  }

  const d = dashRes.data;

  document.getElementById("cardCropHealth").innerHTML = `${d.crop_health} <span class="unit">%</span>`;
  document.getElementById("cardSoilMoisture").innerHTML = `${d.soil_moisture} <span class="unit">%</span>`;
  document.getElementById("cardTemperature").innerHTML = `${d.temperature} <span class="unit">°C</span>`;
  document.getElementById("cardHumidity").innerHTML = `${d.humidity} <span class="unit">%</span>`;

  const on = d.irrigation_status === "ON";
  document.getElementById("cardIrrigation").innerHTML = on
    ? `<span class="pill pill-info">💧 ON</span>`
    : `<span class="pill pill-neutral">OFF</span>`;

  document.getElementById("cardDiseaseRisk").innerHTML =
    `<span class="pill ${riskPillClass(d.disease_risk)}">${d.disease_risk}</span>`;

  // Crop overview
  document.getElementById("overviewCropName").textContent = d.crop.name;
  document.getElementById("overviewGrowthStage").textContent = d.crop.growth_stage;
  document.getElementById("overviewHealthPct").textContent = `${d.crop.health_pct}%`;
  document.getElementById("overviewSoilCondition").textContent = d.crop.soil_condition;
  document.getElementById("fieldChip").querySelector(".field-crop").textContent = `· ${d.crop.name} Crop`;

  // Alerts (dashboard card + notification dropdown)
  const alertsList = document.getElementById("alertsList");
  const notifList = document.getElementById("notifList");
  const notifBadge = document.getElementById("notifBadge");

  if (d.alerts && d.alerts.length) {
    alertsList.innerHTML = d.alerts.map(a => `
      <div class="alert-item">
        <div class="alert-dot ${alertDotClass(a.level)}"></div>
        <div>
          <div class="alert-text">${escapeHtml(a.message)}</div>
          <div class="alert-time">${fmtTime(a.timestamp)}</div>
        </div>
      </div>
    `).join("");

    notifList.innerHTML = d.alerts.map(a => `
      <div class="dropdown-item" style="white-space:normal; line-height:1.4;">
        <div class="alert-dot ${alertDotClass(a.level)}" style="display:inline-block; margin-right:6px;"></div>
        ${escapeHtml(a.message)}
      </div>
    `).join("");
    notifBadge.style.display = "inline-block";
  } else {
    alertsList.innerHTML = `<div class="state-box"><span class="state-icon">✅</span>No active alerts right now.</div>`;
    notifList.innerHTML = `<div class="dropdown-item">No new notifications.</div>`;
    notifBadge.style.display = "none";
  }

  // Weather
  if (weatherRes.ok && weatherRes.data) {
    const w = weatherRes.data;
    document.getElementById("weatherTemp").textContent = `${w.temperature}°C`;
    document.getElementById("weatherHumidity").textContent = `${w.humidity}%`;
    document.getElementById("weatherRain").textContent = `${w.rain_probability}%`;
    document.getElementById("weatherWind").textContent = `${w.wind_speed} km/h`;
    document.getElementById("weatherCondition").textContent = w.condition;
  }

  document.getElementById("loadingState").style.display = "none";
  document.getElementById("dashboardContent").style.display = "block";
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// Logout link inside the profile dropdown (separate id from sidebar logout)
document.getElementById("logoutBtnDropdown")?.addEventListener("click", (e) => {
  e.preventDefault();
  logout();
});

document.addEventListener("DOMContentLoaded", loadDashboard);
