from __future__ import annotations

from datetime import datetime
import io
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def format_iso_timestamp(iso_str: str) -> str:
    """Format ISO 8601 timestamp string into a human-readable date format."""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y, %I:%M %p UTC")
    except Exception:
        return iso_str


def get_risk_tier_color(tier: str) -> colors.Color:
    """Return colored Hex mapping for risk levels."""
    tier_upper = tier.upper()
    if tier_upper == "HIGH":
        return colors.HexColor("#ef4444")
    if tier_upper == "MEDIUM":
        return colors.HexColor("#f59e0b")
    return colors.HexColor("#10b981")


def get_priority_color(priority: str) -> colors.Color:
    """Return priority colors for table cells."""
    p_upper = priority.upper()
    if p_upper == "CRITICAL":
        return colors.HexColor("#ef4444")
    if p_upper == "IMPORTANT":
        return colors.HexColor("#f59e0b")
    return colors.HexColor("#3b82f6")  # Blue for advisory


def generate_pdf_report(assessment: dict[str, Any]) -> bytes:
    """
    Generate a professional compliance-grade PDF report summarizing the risk assessment
    using ReportLab. Returns the generated document as raw bytes.
    """
    result_data = assessment.get("result_data", {})
    input_data = assessment.get("input_data", {})

    project_name = assessment.get("project_name", "Enterprise Migration")
    created_at_raw = assessment.get("created_at", "")
    created_at = format_iso_timestamp(created_at_raw)
    assessment_id = assessment.get("id", "N/A")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,  # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        name="DocTitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        name="DocSubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=15,
    )

    section_header_style = ParagraphStyle(
        name="SectionHeaderStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        name="BodyTextStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    body_bold_style = ParagraphStyle(
        name="BodyBoldTextStyle",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    header_cell_style = ParagraphStyle(
        name="HeaderCellStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white,
    )

    rec_detail_style = ParagraphStyle(
        name="RecDetailStyle",
        parent=body_style,
        fontSize=8.5,
        leading=12,
    )

    story = []

    # 1. Document Header
    story.append(Paragraph("CLOUD MIGRATION RISK ASSESSMENT REPORT", title_style))
    story.append(Paragraph(f"Project Name: {project_name} | ID: {assessment_id} | Created: {created_at}", subtitle_style))

    # Divider Line
    divider_table = Table([[""]], colWidths=[504])
    divider_table.setStyle(
        TableStyle([
            ("LINEABOVE", (0, 0), (-1, -1), 1.5, colors.HexColor("#6366f1")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    story.append(divider_table)
    story.append(Spacer(1, 10))

    # 2. Section 1: Executive Summary & Dimensions
    story.append(Paragraph("Executive Summary & Risk Metrics", section_header_style))

    tier_val = result_data.get("risk_tier", "LOW")
    tier_color = get_risk_tier_color(tier_val)
    live_pricing_status = "Live API" if result_data.get("live_price_used", False) else "Cache Fallback"

    # Score Summary Table
    metrics_data = [
        [
            Paragraph("Metric Dimension", body_bold_style),
            Paragraph("Risk Score", body_bold_style),
            Paragraph("Risk Classification / Details", body_bold_style)
        ],
        [
            Paragraph("Composite Risk (C)", body_style),
            Paragraph(f"{result_data.get('composite_score', 0.0):.1f}", body_bold_style),
            Paragraph(f"<font color='{tier_color.hexval()}'><b>{tier_val} RISK TIER</b></font>", body_bold_style)
        ],
        [
            Paragraph("Operational Risk (O)", body_style),
            Paragraph(f"{result_data.get('operational_score', 0.0):.1f}", body_style),
            Paragraph("Evaluates complexity, servers, maintenance, and sizes.", body_style)
        ],
        [
            Paragraph("Financial Risk (F)", body_style),
            Paragraph(f"{result_data.get('financial_score', 0.0):.1f}", body_style),
            Paragraph(f"Cost Delta, Egress. Est. Cloud Cost: ${result_data.get('monthly_est_usd', 0.0):,.2f}/mo ({live_pricing_status})", body_style)
        ],
        [
            Paragraph("Cybersecurity Risk (Cy)", body_style),
            Paragraph(f"{result_data.get('cybersec_score', 0.0):.1f}", body_style),
            Paragraph("IAM posture, data sensitivity, encryption, and compliance.", body_style)
        ],
    ]

    metrics_table = Table(metrics_data, colWidths=[150, 80, 274])
    metrics_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(metrics_table)
    story.append(Spacer(1, 14))

    # 3. Section 2: Input Parameters Audit List
    story.append(Paragraph("Assessment Input Configurations", section_header_style))

    # Audit list key-value columns
    input_rows = [
        [
            Paragraph("<b>Parameter Field</b>", body_bold_style),
            Paragraph("<b>Configured Value</b>", body_bold_style),
            Paragraph("<b>Parameter Field</b>", body_bold_style),
            Paragraph("<b>Configured Value</b>", body_bold_style)
        ],
        [
            Paragraph("Data Volume (TB)", body_style), Paragraph(str(input_data.get("data_volume_tb", 0)), body_style),
            Paragraph("AWS Region", body_style), Paragraph(str(input_data.get("target_region", "")), body_style)
        ],
        [
            Paragraph("Server Count", body_style), Paragraph(str(input_data.get("server_count", 0)), body_style),
            Paragraph("Instance Category", body_style), Paragraph(str(input_data.get("resource_type", "")), body_style)
        ],
        [
            Paragraph("Dependency Complexity", body_style), Paragraph(str(input_data.get("app_complexity", "")), body_style),
            Paragraph("Est. Egress (TB)", body_style), Paragraph(str(input_data.get("egress_volume_tb", 0)), body_style)
        ],
        [
            Paragraph("Migration Window (hrs)", body_style), Paragraph(str(input_data.get("migration_window_hrs", 0)), body_style),
            Paragraph("On-Prem CapEx ($/mo)", body_style), Paragraph(f"${input_data.get('capex_monthly_usd', 0.0):,.2f}", body_style)
        ],
        [
            Paragraph("Data Sensitivity", body_style), Paragraph(str(input_data.get("data_sensitivity", "")), body_style),
            Paragraph("Projected Users", body_style), Paragraph(str(input_data.get("projected_users", 0)), body_style)
        ],
        [
            Paragraph("IAM Permissiveness", body_style), Paragraph(str(input_data.get("iam_permissiveness", "")), body_style),
            Paragraph("Encryption Posture", body_style), Paragraph(str(input_data.get("encryption_posture", "")), body_style)
        ],
        [
            Paragraph("Compliance Scope", body_style), Paragraph(str(input_data.get("compliance_scope", "")), body_style),
            Paragraph("—", body_style), Paragraph("—", body_style)
        ]
    ]

    inputs_table = Table(input_rows, colWidths=[140, 112, 140, 112])
    inputs_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(inputs_table)
    story.append(Spacer(1, 14))

    # 4. Section 3: Recommendations Table
    story.append(Paragraph("Actionable Recommendations & Mitigations", section_header_style))

    recs = result_data.get("recommendations", [])
    if not recs:
        story.append(Paragraph("No critical risks exceeded parameters thresholds. Current configuration is within default risk guidelines.", body_style))
    else:
        # Table of Recommendations
        rec_headers = [
            Paragraph("Dimension", header_cell_style),
            Paragraph("Parameter", header_cell_style),
            Paragraph("Priority", header_cell_style),
            Paragraph("Score", header_cell_style),
            Paragraph("Mitigation Detail", header_cell_style)
        ]

        rec_table_rows = [rec_headers]
        for item in recs:
            p_val = item.get("priority", "ADVISORY")
            p_color = get_priority_color(p_val)
            rec_table_rows.append([
                Paragraph(item.get("dimension", ""), body_style),
                Paragraph(item.get("parameter", ""), body_style),
                Paragraph(f"<font color='{p_color.hexval()}'><b>{p_val}</b></font>", body_bold_style),
                Paragraph(f"{item.get('score', 0.0):.1f}", body_style),
                Paragraph(item.get("detail", ""), rec_detail_style)
            ])

        recs_table = Table(rec_table_rows, colWidths=[70, 90, 68, 40, 236])
        recs_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ])
        )
        story.append(recs_table)

    story.append(Spacer(1, 20))
    disclaimer_text = (
        "<i>Disclaimer: This report is a decision-support audit tool generated automatically based on "
        "user-supplied parameters and AWS Pricing endpoints. All results are analytical assessments and "
        "do not constitute formal architectural certifications. Professional engineering judgment "
        "must be applied to all migration workflows.</i>"
    )
    story.append(Paragraph(disclaimer_text, subtitle_style))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
