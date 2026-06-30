# CloudRA — Cloud Migration Risk Assessor

CloudRA is a premium, presentation-ready web application designed to assess, score, and document the risks associated with enterprise cloud migrations. The project aligns with academic specifications across three key risk dimensions: **Operational**, **Financial**, and **Cybersecurity**.

---

## 🌟 Key Features

1. **Thesis-Aligned Scoring Engine**:
   - Computes weighted sub-scores using exact piecewise normalisation formulas for data volume, server count, migration window, monthly cost delta, egress volume, and user load.
   - Applies categorical lookups for application complexity, data sensitivity, IAM permissions, encryption posture, and compliance scopes.
2. **AWS Price Fallback Service**:
   - Queries live Amazon Web Services EC2 pricing metrics dynamically based on target regions and instance sizes (t3 profiles).
   - Operates with a strict **1.5-second latency isolation threshold**. If internet or AWS credentials are unavailable, it falls back seamlessly to cached pricing values.
3. **Audit History Database**:
   - Persists all past migration assessments inside an SQLite database schema.
   - Supports live search, dynamic record loading, and soft deletion of audit logs directly from the sidebar.
4. **Automated PDF Compliance Reports**:
   - Compiles audit scores, input parameters, and sorted mitigation recommendations into print-ready compliance report PDFs on the fly using ReportLab.
5. **Organic Stillwater Design Overhaul**:
   - Warm-beige tactile styling featuring variable-serif displays, high-contrast layouts, and an embedded linen grain texture.
   - **Dynamic Risk Alignment Orb**: A pulsing visual guide in the bottom corner that adjusts its speed and color (sage-green, amber, terracotta) dynamically based on the active risk level.
6. **Public Landing Page & Authentication**:
   - Beautiful, narrative-driven landing page outlining feature sets, workflows, and mathematical dimension formulas.
   - Secure session-based authentication guarding the dashboard.
   - Credentials: **`admin` / `admin`**.
   - Accessible **Sign Out** button in the dashboard topbar.

---

## 📶 Presentation, AWS API Integration & Offline Capability

This application has been engineered to run **100% offline** for smooth, zero-latency presentations, with optional live AWS API capability:
- **AWS API Integration**: Queries real-time EC2 on-demand pricing via Boto3. If credentials are set up, the dashboard displays a "live price" badge.
- **Fail-Safe Fallback**: If offline or credentials are not configured, the AWS pricing service falls back seamlessly to a local JSON cache with a 1.5s timeout.
- **No JS CDN Dependencies**: Charts are drawn using native HTML5 Canvas 2D context algorithms. No external UI or charting libraries are loaded.
- **Offline Fonts**: Variable font formats are loaded locally via `@font-face` mappings in `fonts.css`, ensuring the typography looks identical online or offline.
- **Embedded Textures**: The organic linen grain background is embedded directly in [styles.css](file:///c:/Users/HP/Documents/Codex/2026-06-27/this/frontend/styles.css) as a local base64 SVG data URI.

---

## 🚀 How to Run the App

### 1. Prerequisites
Ensure Python 3.12+ is installed on your local machine.

### 2. Set Up the Environment
Open a terminal in the project root directory and execute:
```bash
# Activate the virtual environment
.venv\Scripts\activate

# Install package dependencies
pip install -r requirements.txt
```

### 3. Run the Development Server
You can launch the server and open the web browser automatically:
- On Windows: Double-click the `start.bat` file in the project root.
- Alternatively, run manually:
  ```bash
  python -m src.cloud_risk.api
  ```
Once started, the application will be hosted at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)** (which serves the landing page. Click *Sign In* or *Launch* and log in using **`admin` / `admin`** to access the dashboard).

### 4. (Optional) Configure Live AWS Pricing
If you want the dashboard to show live price queries instead of the cached tables:
1. Ensure your AWS IAM User has the `AWSPriceListServiceFullAccess` policy attached.
2. Generate an **Access Key ID** and **Secret Access Key** under the user's *Security credentials* tab.
3. Configure them locally by running:
   ```bash
   aws configure
   ```
   Set the Default Region to `us-east-1` (the AWS pricing endpoint is only hosted there).

### 5. Running the Tests
To execute the automated verification test suite (52 tests checking scoring ranges, fallbacks, database transactions, login routing, session status, and PDF generation):
```bash
pytest -v
```
