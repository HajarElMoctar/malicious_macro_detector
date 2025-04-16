from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

import os
from analysis.static_analysis import analyze_vba_macros
from analysis.dynamic_analysis import run_dynamic_analysis
from analysis.threat_score import calculate_threat_score
from analysis.report_generator import generate_pdf_report
from openai_api import ask_gpt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

chat_sessions = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        analysis_types = request.form.get("analysisType", "static").split(",")

        if not file.filename.lower().endswith((".doc", ".docm")):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        report_id = str(uuid4())
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], report_id + "_" + filename)
        file.save(filepath)

        static_result, dynamic_result = {}, {}

        if "static" in analysis_types:
            static_result = analyze_vba_macros(filepath)

        if "dynamic" in analysis_types:
            dynamic_result = run_dynamic_analysis(filepath)

        static_threat_score = calculate_threat_score(static_result) if "static" in analysis_types else None
        dynamic_threat_score = dynamic_result.get("threat_score") if "dynamic" in analysis_types else None
        threat_score = dynamic_threat_score if dynamic_threat_score is not None else static_threat_score

        hybrid_report_url = dynamic_result.get("hybrid_report_url", "")

        # --- ✅ Construct GPT prompt dynamically ---
        sections = ["You are an AI assistant that detects malicious Word macros.\nGenerate a detailed, beginner-friendly report.\n"]

        if "static" in analysis_types:
            static_vba_code = static_result.get("vba_code", "").strip()
            if not static_vba_code:
                static_vba_code = "No VBA macro code was found in the document."
            sections.append(f"### Static Analysis:\n{static_vba_code}")

        if "dynamic" in analysis_types:
            dynamic_summary = dynamic_result.get("summary", "").strip()
            if not dynamic_summary:
                dynamic_summary = "Dynamic analysis was performed, but no behavioral summary was returned."
            sections.append(f"\n\n### Dynamic Analysis:\n{dynamic_summary}")

        if len(sections) == 1:
            sections.append("No analysis was performed on this document.")

        summary_prompt = "\n\n".join(sections)
        summary = ask_gpt(summary_prompt)

        # --- Context to include in chat memory
        context_intro = "Here is the full analysis of the uploaded document:\n"
        context_static = f"📝 Static Analysis VBA Code:\n{static_result.get('vba_code', 'N/A')}" if "static" in analysis_types else ""
        context_dynamic = f"\n\n🧪 Dynamic Analysis Summary:\n{dynamic_result.get('summary', 'N/A')}" if "dynamic" in analysis_types else ""
        context_summary = f"\n\n🧠 GPT Summary:\n{summary}"
        initial_context = context_intro + context_static + context_dynamic + context_summary

        chat_sessions[report_id] = [{"role": "assistant", "content": initial_context.strip()}]

        return jsonify({
            "reportId": report_id,
            "summary": summary,
            "staticThreatScore": static_threat_score if static_threat_score is not None else "N/A",
            "dynamicThreatScore": dynamic_threat_score if dynamic_threat_score is not None else "N/A",
            "threatScore": threat_score if threat_score is not None else "N/A",
            "hybridReportUrl": hybrid_report_url
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Something went wrong while analyzing the file."}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    report_id = data["reportId"]
    message = data["message"]

    history = chat_sessions.get(report_id)
    if not history:
        history = [{
            "role": "assistant",
            "content": (
                "Hi! It looks like the report context is missing. "
                "Please re-upload your document or paste macro code for analysis."
            )
        }]

    history.append({"role": "user", "content": message})
    response = ask_gpt(prompt=None, history=history)
    history.append({"role": "assistant", "content": response})
    chat_sessions[report_id] = history

    return jsonify({"reply": response})

@app.route("/export-report/<report_id>")
def export_report(report_id):
    messages = chat_sessions.get(report_id, [])
    pdf_path = generate_pdf_report(messages, report_id)
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
