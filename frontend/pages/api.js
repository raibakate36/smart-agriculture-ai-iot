<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Crop Health · Smart Agriculture</title>
<link rel="stylesheet" href="../css/style.css" />
<link rel="stylesheet" href="../css/responsive.css" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
<div class="app-shell">
  <div class="sidebar-overlay" id="sidebarOverlay"></div>
  <aside class="sidebar" id="sidebar">
    <div class="brand"><span class="leaf" aria-hidden="true">🌱</span> Smart Agriculture</div>
    <nav aria-label="Main navigation">
      <ul class="nav-list">
        <li><a href="../index.html"><span class="nav-icon">📊</span> Dashboard</a></li>
        <li><a href="disease-detection.html"><span class="nav-icon">📷</span> Disease Detection</a></li>
        <li><a href="irrigation.html"><span class="nav-icon">💧</span> Smart Irrigation</a></li>
        <li><a href="crop-health.html" class="active"><span class="nav-icon">🍅</span> Crop Health</a></li>
        <li><a href="analytics.html"><span class="nav-icon">📈</span> Analytics</a></li>
        <li><a href="settings.html"><span class="nav-icon">⚙️</span> Settings</a></li>
      </ul>
    </nav>
    <div class="sidebar-footer">
      Logged in as <strong data-current-username>Farmer</strong><br/>
      <a href="#" id="logoutBtn" style="color:#E6A25C;">Log out</a>
    </div>
  </aside>

  <div class="main">
    <div class="topbar">
      <div style="display:flex; align-items:center; gap:10px;">
        <button class="menu-toggle" id="menuToggle" aria-label="Open menu">☰</button>
        <div>
          <div class="page-title">Crop Health</div>
          <div class="page-subtitle">Monitor growth, nutrients, and pest risk</div>
        </div>
      </div>
      <div class="field-chip"><span class="dot"></span> FIELD_001 <span class="field-crop">· Tomato Crop</span></div>
    </div>

    <div class="content">
      <div class="demo-banner visible" id="demoBanner">
        <span class="badge">DEMO MODE</span>
        <span>Showing simulated crop health data. Connect a backend to see live readings.</span>
      </div>

      <div class="card" style="margin-bottom:20px;">
        <div class="field-group" style="margin-bottom:0; max-width:280px;">
          <label for="cropSelect">Select Crop</label>
          <select id="cropSelect"></select>
        </div>
      </div>

      <div id="loadingState" class="state-box">
        <div class="spinner"></div>
        <div>Loading crop health...</div>
      </div>

      <div id="healthContent" style="display:none;">

        <div class="grid grid-4">
          <div class="card">
            <span class="card-label">📅 Crop Age</span>
            <div class="metric-value" id="valAge" style="font-size:1.6rem; margin-top:8px;">-- <span class="unit">days</span></div>
          </div>
          <div class="card">
            <span class="card-label">🌱 Growth Stage</span>
            <div class="metric-value" id="valStage" style="font-size:1.4rem; margin-top:8px;">--</div>
          </div>
          <div class="card">
            <span class="card-label">💚 Health Score</span>
            <div class="metric-value" id="valHealthScore" style="font-size:1.6rem; margin-top:8px;">-- <span class="unit">%</span></div>
          </div>
          <div class="card">
            <span class="card-label">🐛 Pest Risk</span>
            <div class="metric-value" id="valPestRisk" style="margin-top:8px;">--</div>
          </div>
        </div>

        <h2 class="section-heading">Growth Timeline</h2>
        <div class="card">
          <div class="timeline" id="growthTimeline"></div>
        </div>

        <h2 class="section-heading">Status Indicators</h2>
        <div class="grid grid-3">
          <div class="card">
            <span class="card-label">🪱 Soil Health</span>
            <div class="bar-track" style="margin-top:12px;"><div class="bar-fill" id="soilHealthBar" style="width:0%;"></div></div>
            <div class="metric-sub" id="soilHealthValue">--%</div>
          </div>
          <div class="card">
            <span class="card-label">🧪 Nutrient Status</span>
            <div class="bar-track" style="margin-top:12px;"><div class="bar-fill" id="nutrientBar" style="width:0%;"></div></div>
            <div class="metric-sub" id="nutrientValue">--%</div>
          </div>
          <div class="card">
            <span class="card-label">💧 Water Status</span>
            <div class="bar-track" style="margin-top:12px;"><div class="bar-fill" id="waterStatusBar" style="width:0%;"></div></div>
            <div class="metric-sub" id="waterStatusValue">--%</div>
          </div>
        </div>
      </div>

      <div id="errorState" class="state-box" style="display:none;">
        <span class="state-icon">⚠️</span>
        <div id="errorMessage">Unable to load crop health data.</div>
        <button class="btn btn-secondary" onclick="loadCropHealth()">Try Again</button>
      </div>

      <footer class="app-footer">Smart Agriculture Monitoring Platform · Prototype build</footer>
    </div>
  </div>
</div>

<script src="../js/api.js"></script>
<script src="../js/auth.js"></script>
<script src="../js/crop-health.js"></script>
</body>
</html>
