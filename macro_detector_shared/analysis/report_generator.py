from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import html


def format_text_as_html(content):
    """Converts raw text to safe HTML and wraps in <pre> for code formatting."""
    escaped = html.escape(content).replace("\n", "<br/>")
    return f'<pre style="font-family: Courier; font-size: 9pt;">{escaped}</pre>'


def generate_pdf_report(messages, report_id):
    filename = f"report_{report_id}.pdf"
    path = os.path.join("static", filename)
    os.makedirs("static", exist_ok=True)

    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="WrappedCode",
        fontName="Courier",
        fontSize=9,
        leading=12,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=0,
        rightIndent=0
    ))

    flowables = []
    flowables.append(Paragraph("🛡️ Full Report & Chat Log", styles["Title"]))
    flowables.append(Spacer(1, 12))

    for msg in messages:
        role = msg.get("role", "Unknown").capitalize()
        content = msg.get("content", "").strip()

        # Heading
        flowables.append(Paragraph(f"<b>{role}:</b>", styles["Heading4"]))

        # Format and wrap code-like content as HTML
        html_content = format_text_as_html(content)
        flowables.append(Paragraph(html_content, styles["WrappedCode"]))
        flowables.append(Spacer(1, 12))

    doc.build(flowables)
    return path
