from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, redirect, session, url_for
from flask_cors import CORS

from .scoring import assess_migration_risk
from .pricing import get_instance_monthly_cost
from .serialization import input_from_dict
from .store import AssessmentStore


def create_app(test_config: dict | None = None) -> Flask:
    static_dir = Path(__file__).resolve().parents[2] / "frontend"
    app = Flask(__name__, static_folder=str(static_dir), static_url_path="/static")
    CORS(app)

    app.secret_key = "cloudra-session-key-2026"

    import os
    use_dynamodb = os.environ.get("USE_DYNAMODB", "false").lower() == "true"

    if test_config:
        app.config.from_mapping(test_config)
        if "USE_DYNAMODB" in test_config:
            use_dynamodb = test_config["USE_DYNAMODB"]

    root_dir = Path(__file__).resolve().parents[2]
    db_path = app.config.get("DATABASE_PATH", str(root_dir / "assessments.db"))
    store = AssessmentStore(db_path, use_dynamodb=use_dynamodb)
    store.init_db()

    # ─── Landing Page (public) ────────────────────────────────────────────────
    @app.get("/")
    def landing():
        return send_from_directory(static_dir, "landing.html")

    # ─── Login Page ───────────────────────────────────────────────────────────
    @app.get("/login")
    def login_page():
        if session.get("authenticated"):
            return redirect("/dashboard")
        return send_from_directory(static_dir, "login.html")

    @app.post("/login")
    def login_submit():
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == "admin" and password == "admin":
            session["authenticated"] = True
            return redirect("/dashboard")
        return redirect("/login?error=1")

    @app.get("/logout")
    def logout():
        session.pop("authenticated", None)
        return redirect("/")

    # ─── Dashboard (protected) ────────────────────────────────────────────────
    @app.get("/dashboard")
    def dashboard():
        if not session.get("authenticated"):
            return redirect("/login")
        return send_from_directory(static_dir, "index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "cloud-risk-api"})

    @app.post("/assessments")
    def create_assessment():
        if not request.is_json:
            return jsonify({"error": "Request body must be JSON"}), 400

        try:
            payload = input_from_dict(request.get_json() or {})

            # Phase 2: Live AWS Pricing API query with cached fallback.
            monthly_cost_usd, live_price_used = get_instance_monthly_cost(
                payload.target_region, payload.resource_type
            )

            result = assess_migration_risk(payload, monthly_cost_usd, live_price_used)
            saved_result = store.save_assessment(payload, result)
        except (TypeError, ValueError, KeyError) as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(saved_result), 201

    @app.get("/assessments")
    def list_assessments():
        try:
            history = store.list_assessments()
            return jsonify(history), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.get("/assessments/<id>")
    def get_assessment(id):
        try:
            assessment = store.get_assessment(id)
            if not assessment:
                return jsonify({"error": f"Assessment with ID {id} not found"}), 404
            return jsonify(assessment), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.get("/assessments/<id>/report")
    def get_assessment_report(id):
        try:
            assessment = store.get_assessment(id)
            if not assessment:
                return jsonify({"error": f"Assessment with ID {id} not found"}), 404

            from .report import generate_pdf_report
            pdf_data = generate_pdf_report(assessment)

            from io import BytesIO
            from flask import send_file
            return send_file(
                BytesIO(pdf_data),
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"CloudRisk_Report_{id}.pdf"
            )
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    @app.delete("/assessments/<id>")
    def delete_assessment(id):
        try:
            deleted = store.delete_assessment(id)
            if not deleted:
                return jsonify({"error": f"Assessment with ID {id} not found"}), 404
            return jsonify({"status": "deleted", "id": id}), 200
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
