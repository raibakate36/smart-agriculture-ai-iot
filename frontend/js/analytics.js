

requireAuth();

let charts = {};

function fmtLabel(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function destroyCharts() {
  Object.values(charts).forEach((c) => c && c.destroy());
  charts = {};
}

function makeLineChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: "index" },
      plugins: { legend: { display: datasets.length > 1, labels: { boxWidth: 12, font: { size: 11 } } } },
      scales: {
        x: { ticks: { maxTicksLimit: 8, font: { size: 10 } }, grid: { display: false } },
        y: { ticks: { font: { size: 10 } }, grid: { color: "#EBE8DA" } },
      },
      elements: { point: { radius: 0 }, line: { tension: 0.35, borderWidth: 2 } },
    },
  });
}

function makeBarChart(canvasId, labels, data, color) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    data: { labels, datasets: [{ label: "Water Usage (L)", data, backgroundColor: color, borderRadius: 4 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { maxTicksLimit: 8, font: { size: 10 } }, grid: { display: false } },
        y: { ticks: { font: { size: 10 } }, grid: { color: "#EBE8DA" } },
      },
    },
  });
}

async function loadAnalytics() {
  document.getElementById("loadingState").style.display = "flex";
  document.getElementById("analyticsContent").style.display = "none";
  document.getElementById("errorState").style.display = "none";

  const rangeDays = parseInt(document.getElementById("rangeSelect").value, 10);
  const result = await getAnalytics(rangeDays);

  if (!result.ok || !result.data) {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "flex";
    document.getElementById("errorMessage").textContent = friendlyErrorMessage(result);
    return;
  }

  const { points, summary } = result.data;
  const labels = points.map((p) => fmtLabel(p.date));

  document.getElementById("avgMoisture").innerHTML = `${summary.avg_soil_moisture} <span class="unit">%</span>`;
  document.getElementById("totalWater").innerHTML = `${summary.total_water_used_l.toLocaleString()} <span class="unit">L</span>`;
  document.getElementById("avgTemp").innerHTML = `${summary.avg_temperature} <span class="unit">°C</span>`;
  document.getElementById("healthTrend").textContent = summary.crop_health_trend;

  destroyCharts();

  charts.moisture = makeLineChart("moistureChart", labels, [{
    label: "Soil Moisture (%)", data: points.map((p) => p.soil_moisture),
    borderColor: "#2E6E8E", backgroundColor: "rgba(46,110,142,0.08)", fill: true,
  }]);

  charts.temp = makeLineChart("tempChart", labels, [{
    label: "Temperature (°C)", data: points.map((p) => p.temperature),
    borderColor: "#C77B2E", backgroundColor: "rgba(199,123,46,0.08)", fill: true,
  }]);

  charts.humidity = makeLineChart("humidityChart", labels, [{
    label: "Humidity (%)", data: points.map((p) => p.humidity),
    borderColor: "#4C7A4F", backgroundColor: "rgba(76,122,79,0.08)", fill: true,
  }]);

  charts.water = makeBarChart("waterChart", labels, points.map((p) => p.water_usage_l), "#6FA9C4");

  charts.health = makeLineChart("healthChart", labels, [{
    label: "Crop Health (%)", data: points.map((p) => p.crop_health),
    borderColor: "#3E7C3E", backgroundColor: "rgba(62,124,62,0.08)", fill: true,
  }]);

  charts.disease = makeLineChart("diseaseChart", labels, [{
    label: "Disease Risk (%)", data: points.map((p) => p.disease_risk),
    borderColor: "#B23A32", backgroundColor: "rgba(178,58,50,0.08)", fill: true,
  }]);

  document.getElementById("loadingState").style.display = "none";
  document.getElementById("analyticsContent").style.display = "block";
}

document.getElementById("rangeSelect")?.addEventListener("change", loadAnalytics);
document.addEventListener("DOMContentLoaded", loadAnalytics);

