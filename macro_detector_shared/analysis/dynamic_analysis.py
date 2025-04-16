import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("HYBRID_API_KEY")
SUBMIT_URL = "https://www.hybrid-analysis.com/api/v2/submit/file"
SUMMARY_URL = "https://www.hybrid-analysis.com/api/v2/report"

def run_dynamic_analysis(file_path):
    if not API_KEY:
        return {"summary": "Hybrid Analysis API key is missing."}

    headers = {
        "api-key": API_KEY,
        "User-Agent": "Falcon Sandbox"
    }

    try:
        print("[Dynamic] Submitting file to Hybrid Analysis...")
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {"environment_id": 160}  # Windows 7 64-bit

            submit_res = requests.post(SUBMIT_URL, headers=headers, files=files, data=data)

        print(f"[Dynamic] Submit status: {submit_res.status_code}")
        print(f"[Dynamic] Submit response: {submit_res.text}")

        if submit_res.status_code not in (200, 201):
            return {"summary": "Failed to submit to Hybrid Analysis."}

        response_data = submit_res.json()
        job_id = response_data.get("job_id")
        sha256 = response_data.get("sha256")

        if not job_id or not sha256:
            return {"summary": "Submission succeeded but required values were not returned."}

        print(f"[Dynamic] Job ID: {job_id}")
        print(f"[Dynamic] SHA256: {sha256}")
        print("[Dynamic] Polling /report/{job_id}/summary for up to 10 minutes...")

        for attempt in range(40):  # 10 minutes total
            report_res = requests.get(f"{SUMMARY_URL}/{job_id}/summary", headers=headers)

            if report_res.status_code == 200:
                print(f"[Dynamic] Summary report ready (attempt {attempt + 1})")
                try:
                    return format_summary_output(report_res.json(), sha256)
                except Exception as e:
                    print(f"[Dynamic] Error formatting summary: {str(e)}")
                    return {
                        "summary": (
                            f"Report received but couldn't be processed due to formatting issue: {str(e)}"
                        ),
                        "hybrid_report_url": f"https://www.hybrid-analysis.com/sample/{sha256}",
                        "threat_score": 0
                    }

            print(f"[Dynamic] Report not ready (attempt {attempt + 1})...")
            time.sleep(15)

        return {
            "summary": (
                "Dynamic analysis timed out after 10 minutes. "
                f"You can check the report manually: https://www.hybrid-analysis.com/sample/{sha256}"
            ),
            "hybrid_report_url": f"https://www.hybrid-analysis.com/sample/{sha256}",
            "threat_score": 0
        }

    except Exception as e:
        return {"summary": f"Dynamic analysis failed: {str(e)}"}


def format_summary_output(data, sha256):
    """Format and safely handle missing keys in the report data."""
    verdict = data.get("verdict")
    verdict = verdict.capitalize() if isinstance(verdict, str) else "Unknown"

    threats = data.get("threat_score")
    threats = threats if isinstance(threats, int) else 0

    tags = data.get("classification_tags", [])
    env = data.get("environment_description", "N/A")
    report_link = f"https://www.hybrid-analysis.com/sample/{sha256}"

    summary_lines = [
        f"Verdict: {verdict}",
        f"Threat Score: {threats}",
        f"Environment: {env}",
        "",
        "Classification Tags:",
        ", ".join(tags) if tags else "None",
        "",
        f"View Full Report: {report_link}"
    ]

    return {
        "summary": "\n".join(summary_lines),
        "hybrid_report_url": report_link,
        "threat_score": threats
    }
