// ─── DOM References ──────────────────────────────────────────────────────────

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

// ─── Application State ───────────────────────────────────────────────────────

let activeAssessmentId = null;
let historyList = [];

// ─── Payload Collection ──────────────────────────────────────────────────────

function val(id) {
  return document.querySelector(id).value;
}

function numVal(id) {
  return Number(document.querySelector(id).value);
}

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

// ─── Display Helpers ─────────────────────────────────────────────────────────

const TIER_DISPLAY = { LOW: "Low", MEDIUM: "Medium", HIGH: "High" };

function tierClass(tier) {
  if (tier === "HIGH") return "tier-high";
  if (tier === "MEDIUM") return "tier-medium";
  return "tier-low";
}

function tierColor(tier) {
  if (tier === "HIGH") return "#ef4444";
  if (tier === "MEDIUM") return "#f59e0b";
  return "#10b981";
}

function formatDate(isoString) {
  try {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
      month: "short", day: "numeric", hour: "numeric", minute: "2-digit",
    });
  } catch (e) {
    return isoString;
  }
}

// ─── Canvas Charts ───────────────────────────────────────────────────────────

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

  // Stillwater-aligned risk indicators
  let activeColor = "#5d6e5a"; // Sage deep for low risk
  if (score >= 70) activeColor = "#8e4f33"; // Terracotta deep for high
  else if (score >= 40) activeColor = "#b16a48"; // Terracotta for medium

  ctx.clearRect(0, 0, width, height);

  // Background track (soft ink line)
  ctx.beginPath();
  ctx.strokeStyle = "rgba(44, 38, 32, 0.08)";
  ctx.lineWidth = 12;
  ctx.lineCap = "round";
  ctx.arc(centerX, centerY, radius, startAngle, endAngle);
  ctx.stroke();

  // Active arc (no glow shadows for organic/editorial look)
  ctx.beginPath();
  ctx.strokeStyle = activeColor;
  ctx.lineWidth = 12;
  ctx.lineCap = "round";
  ctx.arc(centerX, centerY, radius, startAngle, valueAngle);
  ctx.stroke();

  // Score text (Ink display font)
  ctx.fillStyle = "#2c2620";
  ctx.font = "300 44px 'Fraunces', serif";
  ctx.textAlign = "center";
  ctx.fillText(String(Math.round(score)), centerX, centerY - 28);

  // Label
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

  // Concentric rings
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

  // Axis lines and labels
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

  // Data polygon (Terracotta themed)
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

  // Vertex dots
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

// ─── Recommendations ─────────────────────────────────────────────────────────

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

// ─── Result Rendering ────────────────────────────────────────────────────────

function renderResult(result) {
  // Score cards
  Object.entries(scoreEls).forEach(([key, el]) => {
    if (el) el.textContent = Number(result[key]).toFixed(1);
  });

  // Header
  activeProjectTitle.textContent = result.project_name;
  tierBadge.textContent = `${TIER_DISPLAY[result.risk_tier] || result.risk_tier} Risk`;
  tierBadge.className = `tier-badge ${tierClass(result.risk_tier)}`;

  // Pricing status
  if (result.live_price_used) {
    pricingBadge.textContent = "AWS Pricing: Live";
    pricingBadge.className = "pricing-badge pricing-live";
  } else {
    pricingBadge.textContent = "AWS Pricing: Cache (Offline)";
    pricingBadge.className = "pricing-badge pricing-offline";
  }
  monthlyEstEl.textContent = `$${Number(result.monthly_est_usd).toFixed(2)} /mo est.`;

  // Charts
  drawGauge(result.composite_score);
  drawRadar(result);

  // Recommendations
  renderRecommendations(result.recommendations);

  // Report Download visibility
  if (activeAssessmentId) {
    btnDownloadReport.style.display = "inline-flex";
  } else {
    btnDownloadReport.style.display = "none";
  }

  // Update Breathing Risk Alignment guide
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

// ─── History Functions ───────────────────────────────────────────────────────

async function fetchHistory() {
  try {
    const response = await fetch("/assessments");
    if (!response.ok) throw new Error("Could not fetch assessment log");
    historyList = await response.json();
    renderHistoryList();
  } catch (error) {
    console.error("History fetch error:", error);
  }
}

function renderHistoryList() {
  historyListEl.innerHTML = "";
  const filterText = historySearchInput.value.toLowerCase().trim();
  const filtered = historyList.filter(item =>
    item.project_name.toLowerCase().includes(filterText)
  );

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

async function loadAssessment(id) {
  try {
    statusMessage.textContent = "Loading record...";
    const response = await fetch(`/assessments/${id}`);
    if (!response.ok) throw new Error("Could not load assessment details");
    const data = await response.json();
    activeAssessmentId = id;
    populateForm(data.input_data);
    renderResult(data.result_data);
    renderHistoryList();
    statusMessage.textContent = "Record loaded.";
  } catch (error) {
    statusMessage.textContent = `Error: ${error.message}`;
  }
}

async function deleteAssessment(id) {
  if (!confirm("Delete this assessment from the audit log?")) return;
  try {
    statusMessage.textContent = "Deleting record...";
    const response = await fetch(`/assessments/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Deletion request failed");
    statusMessage.textContent = "Record deleted.";
    if (activeAssessmentId === id) {
      activeAssessmentId = null;
    }
    await fetchHistory();
  } catch (error) {
    statusMessage.textContent = `Error: ${error.message}`;
  }
}

// ─── Assessment Execution ────────────────────────────────────────────────────

async function runAssessment() {
  statusMessage.textContent = "Calculating risk model...";
  try {
    const payload = collectPayload();
    const response = await fetch("/assessments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Risk calculation failed");

    if (data.id) activeAssessmentId = data.id;
    renderResult(data);
    statusMessage.textContent = "Assessment complete.";
    await fetchHistory();
  } catch (error) {
    statusMessage.textContent = `Error: ${error.message}`;
  }
}

function resetFormToDefaults() {
  activeAssessmentId = null;
  form.reset();
  activeProjectTitle.textContent = "New Migration Assessment";
  tierBadge.textContent = "Low Risk";
  tierBadge.className = "tier-badge tier-low";
  btnDownloadReport.style.display = "none";
  runAssessment();
}

// ─── Event Listeners ─────────────────────────────────────────────────────────

form.addEventListener("submit", (e) => {
  e.preventDefault();
  runAssessment();
});

btnNewAssessment.addEventListener("click", () => resetFormToDefaults());
btnDownloadReport.addEventListener("click", () => {
  if (activeAssessmentId) {
    window.location.href = `/assessments/${activeAssessmentId}/report`;
  }
});
historySearchInput.addEventListener("input", () => renderHistoryList());

// ─── Initialisation ──────────────────────────────────────────────────────────

async function initializeApp() {
  drawGauge(0);
  drawRadar({ operational_score: 0, financial_score: 0, cybersec_score: 0 });
  await fetchHistory();
  if (historyList.length > 0) {
    await loadAssessment(historyList[0].id);
  } else {
    await runAssessment();
  }
}

initializeApp();
