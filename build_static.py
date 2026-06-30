import os
import shutil
import re

def build():
    print("Starting static build for GitHub Pages...")
    
    src_dir = "frontend"
    dest_dir = "docs"
    
    # 1. Recreate docs directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "static"), exist_ok=True)
    
    # 2. Copy fonts and CSS files
    shutil.copytree(os.path.join(src_dir, "static", "fonts"), os.path.join(dest_dir, "static", "fonts"))
    shutil.copy(os.path.join(src_dir, "static", "fonts.css"), os.path.join(dest_dir, "static", "fonts.css"))
    shutil.copy(os.path.join(src_dir, "styles.css"), os.path.join(dest_dir, "static", "styles.css"))
    shutil.copy(os.path.join(src_dir, "landing.css"), os.path.join(dest_dir, "static", "landing.css"))
    
    # Helper to rewrite absolute /static/ references to relative static/
    def clean_html(content, is_login=False, is_dashboard=False):
        content = content.replace('href="/static/', 'href="static/')
        content = content.replace('src="/static/', 'src="static/')
        content = content.replace('href="/"', 'href="index.html"')
        content = content.replace('href="/login"', 'href="login.html"')
        content = content.replace('href="/logout"', 'href="index.html"')
        
        if is_login:
            # Inject a client-side mock login logic into login.html instead of POSTing to /login
            login_js = """
            <script>
              document.getElementById('login-form').addEventListener('submit', function(e) {
                e.preventDefault();
                const u = this.elements['username'].value;
                const p = this.elements['password'].value;
                if (u === 'admin' && p === 'admin') {
                  localStorage.setItem('authenticated', 'true');
                  window.location.href = 'dashboard.html';
                } else {
                  document.getElementById('login-error').classList.add('is-visible');
                }
              });
              
              if (window.location.search.includes('error=1')) {
                document.getElementById('login-error').classList.add('is-visible');
              }
            </script>
            """
            # Replace form submission action and strip POST method
            content = content.replace('<form class="login-form" method="POST" action="/login" id="login-form">', 
                                      '<form class="login-form" id="login-form">')
            content = content.replace('</body>', login_js + '</body>')
            
        if is_dashboard:
            # Add simple gate to dashboard.html to prevent access without mock login
            gate_js = """
            <script>
              if (localStorage.getItem('authenticated') !== 'true') {
                window.location.href = 'login.html';
              }
              // Set up mock PDF download button trigger
              document.getElementById('btn-download-report').addEventListener('click', function(e) {
                e.preventDefault();
                alert('Academic PDF Report Generation is supported locally via the ReportLab backend! In this static GitHub Pages preview, the PDF endpoint is simulated.');
              });
            </script>
            """
            # Replace sign-out link with local storage clear
            content = content.replace('href="/logout"', 'href="index.html" onclick="localStorage.removeItem(\'authenticated\')"')
            content = content.replace('</body>', gate_js + '</body>')
            
        return content

    # 3. Process landing.html -> index.html
    with open(os.path.join(src_dir, "landing.html"), "r", encoding="utf-8") as f:
        landing_content = f.read()
    landing_content = clean_html(landing_content)
    with open(os.path.join(dest_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(landing_content)
        
    # 4. Process login.html -> login.html
    with open(os.path.join(src_dir, "login.html"), "r", encoding="utf-8") as f:
        login_content = f.read()
    login_content = clean_html(login_content, is_login=True)
    with open(os.path.join(dest_dir, "login.html"), "w", encoding="utf-8") as f:
        f.write(login_content)

    # 5. Process index.html -> dashboard.html
    with open(os.path.join(src_dir, "index.html"), "r", encoding="utf-8") as f:
        dashboard_content = f.read()
    dashboard_content = clean_html(dashboard_content, is_dashboard=True)
    with open(os.path.join(dest_dir, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(dashboard_content)

    # 6. Create static app.js containing client-side scoring logic
    write_static_js(os.path.join(dest_dir, "static", "app.js"))
    print("Static build completed successfully in the docs/ folder!")

def write_static_js(output_path):
    # This writes a fully functional mock app.js containing the client-side piecewise normalisation scoring math
    static_js_content = """// CloudRA Static Presentation Mode JavaScript
// Runs 100% Client-Side for GitHub Pages without requiring a backend server.

const form = document.querySelector("#assessment-form");
const statusMessage = document.querySelector("#status-message");
const historyListEl = document.querySelector("#history-list");
const historyEmptyState = document.querySelector("#history-empty-state");
const historySearchInput = document.querySelector("#history-search");
const activeProjectTitle = document.querySelector("#active-project-title");
const tierBadge = document.querySelector("#tier-badge");
const btnNewAssessment = document.querySelector("#btn-new-assessment");
const btnDownloadReport = document.querySelector("#btn-download-report");
const recommendationList = document.querySelector("#recommendation-list");
const gaugeCanvas = document.querySelector("#gauge-chart");
const radarCanvas = document.querySelector("#radar-chart");
const pricingBadge = document.querySelector("#pricing-status-badge");
const monthlyEstEl = document.querySelector("#monthly-est-usd");

const scoreEls = {
  composite_score: document.querySelector("#composite-score"),
  operational_score: document.querySelector("#operational-score"),
  financial_score: document.querySelector("#financial-score"),
  cybersec_score: document.querySelector("#cybersec-score"),
};

const breathOrb = document.querySelector("#breath-orb");
const breathPhase = document.querySelector("#breath-phase");

let activeAssessmentId = null;
let historyList = [];

// Fallback pricing configuration mapping
const PRICING_CACHE = {
  "us-east-1": { EC2_SMALL: 15.18, EC2_MEDIUM: 30.37, EC2_LARGE: 60.74, EC2_XLARGE: 121.47 },
  "us-west-2": { EC2_SMALL: 16.22, EC2_MEDIUM: 32.44, EC2_LARGE: 64.88, EC2_XLARGE: 129.76 },
  "eu-west-1": { EC2_SMALL: 16.64, EC2_MEDIUM: 33.29, EC2_LARGE: 66.58, EC2_XLARGE: 133.15 },
  "ap-southeast-1": { EC2_SMALL: 18.40, EC2_MEDIUM: 36.79, EC2_LARGE: 73.58, EC2_XLARGE: 147.17 }
};

function val(id) { return document.querySelector(id).value; }
function numVal(id) { return Number(document.querySelector(id).value); }

function collectPayload() {
  return {
    project_name: val("#project_name").trim(),
    data_volume_tb: numVal("#data_volume_tb"),
    server_count: numVal("#server_count"),
    app_complexity: val("#app_complexity"),
    migration_window_hrs: numVal("#migration_window_hrs"),
    resource_type: val("#resource_type"),
    target_region: val("#target_region"),
    egress_volume_tb: numVal("#egress_volume_tb"),
    capex_monthly_usd: numVal("#capex_monthly_usd"),
    projected_users: numVal("#projected_users"),
    data_sensitivity: val("#data_sensitivity"),
    iam_permissiveness: val("#iam_permissiveness"),
    encryption_posture: val("#encryption_posture"),
    compliance_scope: val("#compliance_scope"),
  };
}

function populateForm(inputData) {
  document.querySelector("#project_name").value = inputData.project_name || "";
  document.querySelector("#data_volume_tb").value = inputData.data_volume_tb ?? 15;
  document.querySelector("#server_count").value = inputData.server_count ?? 30;
  document.querySelector("#app_complexity").value = inputData.app_complexity || "MEDIUM";
  document.querySelector("#migration_window_hrs").value = inputData.migration_window_hrs ?? 24;
  document.querySelector("#resource_type").value = inputData.resource_type || "EC2_MEDIUM";
  document.querySelector("#target_region").value = inputData.target_region || "eu-west-1";
  document.querySelector("#egress_volume_tb").value = inputData.egress_volume_tb ?? 2.0;
  document.querySelector("#capex_monthly_usd").value = inputData.capex_monthly_usd ?? 3000;
  document.querySelector("#projected_users").value = inputData.projected_users ?? 500;
  document.querySelector("#data_sensitivity").value = inputData.data_sensitivity || "CONFIDENTIAL";
  document.querySelector("#iam_permissiveness").value = inputData.iam_permissiveness || "MODERATE";
  document.querySelector("#encryption_posture").value = inputData.encryption_posture || "FULL";
  document.querySelector("#compliance_scope").value = inputData.compliance_scope || "SINGLE";
}

const TIER_DISPLAY = { LOW: "Low", MEDIUM: "Medium", HIGH: "High" };
function tierClass(tier) {
  return tier === "HIGH" ? "tier-high" : (tier === "MEDIUM" ? "tier-medium" : "tier-low");
}

function formatDate(isoString) {
  try {
    return new Date(isoString).toLocaleString(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  } catch (e) { return isoString; }
}

// ─── Mathematical Scoring Logic Ported to JS ──────────────────────────────────
function normalise(val, scale) {
  for (let s of scale) {
    if (val >= s.min && val <= s.max) {
      if (s.max === s.min) return s.out_min;
      const progress = (val - s.min) / (s.max - s.min);
      return s.out_min + progress * (s.out_max - s.out_min);
    }
  }
  return 1.0;
}

function calculateClientScores(p) {
  // 1. Operational Scoring
  const n_vol = normalise(p.data_volume_tb, [
    { min: 0, max: 10, out_min: 0, out_max: 0.4 },
    { min: 10, max: 100, out_min: 0.4, out_max: 0.8 },
    { min: 100, max: 1000, out_min: 0.8, out_max: 1.0 }
  ]);
  const n_servers = normalise(p.server_count, [
    { min: 0, max: 50, out_min: 0, out_max: 0.5 },
    { min: 50, max: 200, out_min: 0.5, out_max: 0.85 },
    { min: 200, max: 2000, out_min: 0.85, out_max: 1.0 }
  ]);
  const complexity_lookup = { LOW: 0.1, MEDIUM: 0.4, HIGH: 0.8, VERY_HIGH: 1.0 };
  const n_complexity = complexity_lookup[p.app_complexity] || 0.4;
  const n_window = normalise(p.migration_window_hrs, [
    { min: 0, max: 12, out_min: 1.0, out_max: 0.8 },
    { min: 12, max: 48, out_min: 0.8, out_max: 0.3 },
    { min: 48, max: 168, out_min: 0.3, out_max: 0.0 }
  ]);
  const operational_score = (0.30 * n_vol + 0.25 * n_servers + 0.30 * n_complexity + 0.15 * n_window) * 100;

  // 2. Financial Scoring
  const region_pricing = PRICING_CACHE[p.target_region] || PRICING_CACHE["us-east-1"];
  const monthly_instance_cost = region_pricing[p.resource_type] || 30.37;
  const raw_monthly_cost = monthly_instance_cost * p.server_count;
  const n_cost = normalise(raw_monthly_cost, [
    { min: 0, max: 2000, out_min: 0, out_max: 0.4 },
    { min: 2000, max: 10000, out_min: 0.4, out_max: 0.85 },
    { min: 10000, max: 100000, out_min: 0.85, out_max: 1.0 }
  ]);
  const n_egress = normalise(p.egress_volume_tb, [
    { min: 0, max: 50, out_min: 0, out_max: 1.0 }
  ]);
  const delta = raw_monthly_cost - p.capex_monthly_usd;
  const n_delta = normalise(delta, [
    { min: -10000, max: 0, out_min: 0, out_max: 0.3 },
    { min: 0, max: 20000, out_min: 0.3, out_max: 1.0 }
  ]);
  const financial_score = (0.45 * n_cost + 0.30 * n_egress + 0.25 * n_delta) * 100;

  // 3. Cybersecurity Scoring
  const sensitivity_lookup = { PUBLIC: 0.0, INTERNAL: 0.3, CONFIDENTIAL: 0.7, RESTRICTED: 1.0 };
  const n_sens = sensitivity_lookup[p.data_sensitivity] || 0.7;
  const iam_lookup = { LEAST_PRIV: 0.0, MODERATE: 0.3, PERMISSIVE: 0.7, WILDCARD: 1.0 };
  const n_iam = iam_lookup[p.iam_permissiveness] || 0.3;
  const enc_lookup = { FULL: 0.0, PARTIAL: 0.4, TRANSIT_ONLY: 0.7, NONE: 1.0 };
  const n_enc = enc_lookup[p.encryption_posture] || 0.4;
  const compliance_lookup = { NONE: 0.0, SINGLE: 0.3, MULTIPLE: 0.7, CRITICAL: 1.0 };
  const n_comp = compliance_lookup[p.compliance_scope] || 0.3;
  const cybersec_score = (0.35 * n_sens + 0.30 * n_iam + 0.20 * n_enc + 0.15 * n_comp) * 100;

  // 4. Composite Risk Score
  const composite_score = 0.35 * operational_score + 0.30 * financial_score + 0.35 * cybersec_score;
  const risk_tier = composite_score >= 70 ? "HIGH" : (composite_score >= 40 ? "MEDIUM" : "LOW");

  // 5. Generate mitigation recommendations
  const recommendations = [];
  if (operational_score > 60) {
    recommendations.push({
      parameter: "App Complexity",
      dimension: "Operational",
      priority: "CRITICAL",
      detail: "Deconstruct tight application dependencies and perform pre-migration refactoring to mitigate operational downtime."
    });
  }
  if (financial_score > 50) {
    recommendations.push({
      parameter: "Cloud Cost Delta",
      dimension: "Financial",
      priority: "IMPORTANT",
      detail: "Operational cost exceeds on-premises budgets. Recommend purchasing Savings Plans or EC2 Reserved Instances."
    });
  }
  if (n_iam > 0.6) {
    recommendations.push({
      parameter: "IAM Scope",
      dimension: "Cybersecurity",
      priority: "CRITICAL",
      detail: "Permissive/wildcard credentials detected. Enforce IAM boundary checks and migrate to Principle of Least Privilege."
    });
  }
  if (n_enc > 0.5) {
    recommendations.push({
      parameter: "Data Security",
      dimension: "Cybersecurity",
      priority: "IMPORTANT",
      detail: "Enforce complete encryption-at-rest using KMS Keys to cover sensitive data segments."
    });
  }

  return {
    composite_score,
    operational_score,
    financial_score,
    cybersec_score,
    risk_tier,
    live_price_used: false,
    monthly_est_usd: raw_monthly_cost,
    recommendations
  };
}

// ─── Drawing Charts ──────────────────────────────────────────────────────────
function drawGauge(score) {
  const ctx = gaugeCanvas.getContext("2d");
  const width = gaugeCanvas.width;
  const height = gaugeCanvas.height;
  const centerX = width / 2;
  const centerY = height - 20;
  const radius = 110;
  const startAngle = Math.PI;
  const endAngle = 2 * Math.PI;
  const scoreRatio = Math.max(0, Math.min(100, score)) / 100;
  const valueAngle = startAngle + Math.PI * scoreRatio;

  let activeColor = "#5d6e5a";
  if (score >= 70) activeColor = "#8e4f33";
  else if (score >= 40) activeColor = "#b16a48";

  ctx.clearRect(0, 0, width, height);

  ctx.beginPath();
  ctx.strokeStyle = "rgba(44, 38, 32, 0.08)";
  ctx.lineWidth = 12;
  ctx.lineCap = "round";
  ctx.arc(centerX, centerY, radius, startAngle, endAngle);
  ctx.stroke();

  ctx.beginPath();
  ctx.strokeStyle = activeColor;
  ctx.lineWidth = 12;
  ctx.lineCap = "round";
  ctx.arc(centerX, centerY, radius, startAngle, valueAngle);
  ctx.stroke();

  ctx.fillStyle = "#2c2620";
  ctx.font = "300 44px 'Fraunces', serif";
  ctx.textAlign = "center";
  ctx.fillText(String(Math.round(score)), centerX, centerY - 28);

  ctx.fillStyle = "#7a6e60";
  ctx.font = "600 10px 'Inter', sans-serif";
  ctx.fillText("COMPOSITE RISK", centerX, centerY - 8);
}

function drawRadar(scores) {
  const ctx = radarCanvas.getContext("2d");
  const width = radarCanvas.width;
  const height = radarCanvas.height;
  const centerX = width / 2;
  const centerY = height / 2 + 10;
  const radius = 80;
  const labels = ["Operational", "Financial", "Cybersecurity"];
  const values = [
    scores.operational_score,
    scores.financial_score,
    scores.cybersec_score,
  ];

  ctx.clearRect(0, 0, width, height);

  for (let r = 1; r <= 4; r++) {
    ctx.beginPath();
    labels.forEach((_, i) => {
      const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
      const x = centerX + Math.cos(angle) * radius * (r / 4);
      const y = centerY + Math.sin(angle) * radius * (r / 4);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.strokeStyle = "rgba(44, 38, 32, 0.06)";
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  labels.forEach((label, i) => {
    const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + Math.cos(angle) * radius, centerY + Math.sin(angle) * radius);
    ctx.strokeStyle = "rgba(44, 38, 32, 0.12)";
    ctx.stroke();

    const labelDist = radius + 20;
    const labelX = centerX + Math.cos(angle) * labelDist;
    const labelY = centerY + Math.sin(angle) * labelDist + (i === 0 ? -4 : 6);
    ctx.fillStyle = "#7a6e60";
    ctx.font = "600 9px 'Inter', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(label.toUpperCase(), labelX, labelY);
  });

  ctx.beginPath();
  values.forEach((v, i) => {
    const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
    const d = radius * (Math.max(0, Math.min(100, v)) / 100);
    const x = centerX + Math.cos(angle) * d;
    const y = centerY + Math.sin(angle) * d;
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  });
  ctx.closePath();
  ctx.fillStyle = "rgba(177, 106, 72, 0.12)";
  ctx.strokeStyle = "#b16a48";
  ctx.lineWidth = 2;
  ctx.fill();
  ctx.stroke();

  values.forEach((v, i) => {
    const angle = -Math.PI / 2 + (i * 2 * Math.PI) / labels.length;
    const d = radius * (Math.max(0, Math.min(100, v)) / 100);
    const x = centerX + Math.cos(angle) * d;
    const y = centerY + Math.sin(angle) * d;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fillStyle = "#6366f1";
    ctx.stroke();
    ctx.fill();
  });
}

function renderRecommendations(recommendations) {
  recommendationList.innerHTML = "";
  if (!recommendations || recommendations.length === 0) {
    recommendationList.innerHTML = `<li class="rec-item dim-general"><p class="rec-item-detail">No risk indicators exceeded threshold. Current configuration is within acceptable limits.</p></li>`;
    return;
  }
  recommendations.forEach((item) => {
    const li = document.createElement("li");
    const dimClass = `dim-${(item.dimension || "general").toLowerCase()}`;
    const priorityClass = `priority-${(item.priority || "ADVISORY").toLowerCase()}`;
    li.className = `rec-item ${dimClass}`;
    li.innerHTML = `
      <div class="rec-item-header">
        <span class="rec-item-title">${item.parameter}</span>
        <span class="rec-priority-badge ${priorityClass}">${item.priority}</span>
      </div>
      <p class="rec-item-detail">${item.detail}</p>
    `;
    recommendationList.appendChild(li);
  });
}

function renderResult(result) {
  Object.entries(scoreEls).forEach(([key, el]) => {
    if (el) el.textContent = Number(result[key]).toFixed(1);
  });
  activeProjectTitle.textContent = result.project_name;
  tierBadge.textContent = `${TIER_DISPLAY[result.risk_tier] || result.risk_tier} Risk`;
  tierBadge.className = `tier-badge ${tierClass(result.risk_tier)}`;
  pricingBadge.textContent = "AWS Pricing: Cache (Static Mode)";
  pricingBadge.className = "pricing-badge pricing-offline";
  monthlyEstEl.textContent = `$${Number(result.monthly_est_usd).toFixed(2)} /mo est.`;

  drawGauge(result.composite_score);
  drawRadar(result);
  renderRecommendations(result.recommendations);

  btnDownloadReport.style.display = "inline-flex";

  if (breathOrb && breathPhase) {
    const tier = (result.risk_tier || "LOW").toUpperCase();
    if (tier === "HIGH") {
      breathOrb.className = "breath-orb tier-high";
      breathPhase.textContent = "TENSION · RISK ALERT";
    } else if (tier === "MEDIUM") {
      breathOrb.className = "breath-orb tier-medium";
      breathPhase.textContent = "MODERATE · CAUTION";
    } else {
      breathOrb.className = "breath-orb tier-low";
      breathPhase.textContent = "STEADY · OPTIMIZED";
    }
  }
}

// ─── Local Storage Session History ───────────────────────────────────────────
function loadHistoryFromStorage() {
  try {
    const data = localStorage.getItem("assessment_history");
    historyList = data ? JSON.parse(data) : [];
  } catch(e) { historyList = []; }
}

function saveHistoryToStorage() {
  localStorage.setItem("assessment_history", JSON.stringify(historyList));
}

function renderHistoryList() {
  historyListEl.innerHTML = "";
  const filterText = historySearchInput.value.toLowerCase().trim();
  const filtered = historyList.filter(item => item.project_name.toLowerCase().includes(filterText));

  if (filtered.length === 0) {
    historyEmptyState.style.display = "block";
    historyListEl.style.display = "none";
    return;
  }

  historyEmptyState.style.display = "none";
  historyListEl.style.display = "flex";

  filtered.forEach((item) => {
    const li = document.createElement("li");
    const isActive = item.id === activeAssessmentId;
    const scoreVal = Math.round(item.composite_score);
    const badgeClass = `history-item-score ${tierClass(item.risk_tier)}`;

    li.className = `history-item ${isActive ? "active" : ""}`;
    li.innerHTML = `
      <div class="history-item-top">
        <span class="history-item-name" title="${item.project_name}">${item.project_name}</span>
        <span class="${badgeClass}">${scoreVal}</span>
      </div>
      <div class="history-item-bottom">
        <span>${formatDate(item.created_at)}</span>
        <button class="btn-delete-history" data-id="${item.id}" title="Delete assessment">
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    `;

    li.addEventListener("click", () => loadAssessment(item.id));
    li.querySelector(".btn-delete-history").addEventListener("click", (e) => {
      e.stopPropagation();
      deleteAssessment(item.id);
    });
    historyListEl.appendChild(li);
  });
}

function loadAssessment(id) {
  const item = historyList.find(x => x.id === id);
  if (!item) return;
  activeAssessmentId = id;
  populateForm(item.input_data);
  renderResult(item.result_data);
  renderHistoryList();
}

function deleteAssessment(id) {
  if (!confirm("Delete this assessment from the audit log?")) return;
  historyList = historyList.filter(x => x.id !== id);
  saveHistoryToStorage();
  if (activeAssessmentId === id) activeAssessmentId = null;
  renderHistoryList();
  if (historyList.length > 0) {
    loadAssessment(historyList[0].id);
  } else {
    resetFormToDefaults();
  }
}

function runAssessment() {
  statusMessage.textContent = "Calculating client-side risk model...";
  const payload = collectPayload();
  const res = calculateClientScores(payload);
  
  const id = activeAssessmentId || "static-" + Math.random().toString(36).substring(2, 11);
  const created_at = new Date().toISOString();

  const record = {
    id,
    project_name: payload.project_name || "Untitled Project",
    created_at,
    composite_score: res.composite_score,
    risk_tier: res.risk_tier,
    input_data: payload,
    result_data: {
      ...res,
      id,
      created_at
    }
  };

  const existingIdx = historyList.findIndex(x => x.id === id);
  if (existingIdx >= 0) {
    historyList[existingIdx] = record;
  } else {
    historyList.unshift(record);
  }

  activeAssessmentId = id;
  saveHistoryToStorage();
  renderResult(record.result_data);
  renderHistoryList();
  statusMessage.textContent = "Assessment complete (Static Sandbox Mode).";
}

function resetFormToDefaults() {
  activeAssessmentId = null;
  form.reset();
  activeProjectTitle.textContent = "New Migration Assessment";
  tierBadge.textContent = "Low Risk";
  tierBadge.className = "tier-badge tier-low";
  runAssessment();
}

form.addEventListener("submit", (e) => { e.preventDefault(); runAssessment(); });
btnNewAssessment.addEventListener("click", () => resetFormToDefaults());
historySearchInput.addEventListener("input", () => renderHistoryList());

function initializeApp() {
  drawGauge(0);
  drawRadar({ operational_score: 0, financial_score: 0, cybersec_score: 0 });
  loadHistoryFromStorage();
  if (historyList.length > 0) {
    loadAssessment(historyList[0].id);
  } else {
    runAssessment();
  }
}

initializeApp();
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(static_js_content)

if __name__ == "__main__":
    build()
