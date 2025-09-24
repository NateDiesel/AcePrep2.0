
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

def export_cheat_sheet_pdf(
    job_title, job_description, job_role, company_name, user_name,
    questions_top, questions_resume, questions_to_ask, output_path
):
    c = canvas.Canvas(output_path, pagesize=LETTER)
    W, H = LETTER
    x0, y = 0.8*inch, H - 0.9*inch

    def title(text, size=18):
        nonlocal y
        c.setFont("Helvetica-Bold", size)
        c.drawString(x0, y, text); y -= 18

    def line(text, size=11, indent=0, space=14):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(x0 + indent, y, text[:110]); y -= space

    def bullets(items, indent=12):
        for it in items:
            line(f"• {it}", indent=indent)

    c.setFillGray(0.15); c.rect(0, H-0.8*inch, W, 0.8*inch, stroke=0, fill=1)
    c.setFillGray(1); c.setFont("Helvetica-Bold", 20)
    c.drawString(x0, H-0.5*inch, "AcePrep – Interview Cheat Sheet")
    c.setFillGray(0)

    y -= 10
    title("Candidate & Role")
    line(f"Candidate: {user_name or 'N/A'}")
    line(f"Company:  {company_name or 'N/A'}")
    line(f"Job Title: {job_title or 'N/A'}")
    line(f"Interview Role: {job_role or 'N/A'}")
    line(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", space=20)

    title("Role Summary", 14)
    for para in (job_description or "N/A").splitlines():
        if para.strip():
            line(para.strip(), size=10)

    y -= 6; title("Top Interview Questions (Tailored)", 14); bullets(questions_top or [])
    y -= 6; title("Resume-Based Crossover Questions", 14); bullets(questions_resume or [])
    y -= 6; title("Questions to Ask the Interviewer", 14); bullets(questions_to_ask or [])

    c.setFont("Helvetica", 8)
    c.drawRightString(W-0.6*inch, 0.5*inch, "© 2025 AcePrep by Content365.xyz")
    c.save()
