from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from datetime import datetime

def export_cheat_sheet_pdf(job_title, job_description, job_role, company_name, user_name, output_path):
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    def draw_line(text, font="Helvetica", size=12, indent=0, spacing=20):
        nonlocal y
        c.setFont(font, size)
        c.drawString(50 + indent, y, text)
        y -= spacing

    # Header
    draw_line("AcePrep™ Interview Cheat Sheet", "Helvetica-Bold", 16)
    draw_line("by Content365.xyz", "Helvetica", 10, spacing=30)

    # Candidate Info
    draw_line("Candidate Info", "Helvetica-Bold", 12)
    draw_line(f"Candidate: {user_name or 'N/A'}")
    draw_line(f"Job Title: {job_title or 'N/A'}")
    draw_line(f"Company: {company_name or 'N/A'}")
    draw_line(f"Interview Role: {job_role or 'N/A'}", spacing=30)

    # Job + Resume Summary
    draw_line("Job & Resume Summary", "Helvetica-Bold", 12)
    for line in job_description.split("\n"):
        draw_line(line, size=10, spacing=15)
    y -= 10

    # Questions Section
    draw_line("Top Interview Questions (Tailored)", "Helvetica-Bold", 12)
    questions = [
        "Tell me about yourself.",
        "What are your greatest strengths related to this role?",
        "How have your past roles prepared you for this position?",
        "Describe a challenging work situation and how you overcame it.",
        "Why do you want to work at this company?",
        "What do you know about our organization?",
        "How do you handle tight deadlines or pressure?",
        "Describe a time you showed leadership.",
        "Where do you see yourself in five years?",
        "How do you prioritize tasks when everything feels urgent?",
        "Tell me about a time you disagreed with a coworker.",
        "What makes you a strong candidate for this role?",
        "What are your salary expectations?",
        "Do you prefer working alone or on a team?",
        "How do you stay current in your industry?",
        "Give an example of a successful project you led.",
        "What motivates you in your career?",
        "How would your colleagues describe you?",
        "Describe a time you failed and what you learned.",
        "What questions do you have for us?"
    ]
    for q in questions:
        draw_line(f"• {q}", size=10, indent=10, spacing=15)
    y -= 10

    # Ask the Interviewer
    draw_line("Questions to Ask the Interviewer", "Helvetica-Bold", 12)
    for section, qs in {
        "HR": [
            "How would you describe the company culture?",
            "What are the next steps after this interview?"
        ],
        "Manager": [
            "What are the biggest challenges the team is facing?",
            "How is performance typically measured in this role?"
        ],
        "CEO": [
            "What’s your long-term vision for the company?",
            "How does this role contribute to the overall mission?"
        ]
    }.items():
        draw_line(f"{section}:", "Helvetica-Bold", 11)
        for q in qs:
            draw_line(f"- {q}", size=10, indent=10, spacing=15)
        y -= 10

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, 30, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    c.save()
