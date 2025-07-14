from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.utils.parser import extract_resume_context, extract_job_description_from_url
from app.utils.generate_cheat_sheet import generate_cheat_sheet  # GPT logic
from app.utils.pdf_generator import export_cheat_sheet_pdf        # PDF writer
from app.utils.payment_and_email import send_pdf_email
from app.utils.stripe_checkout import create_checkout_session
from dotenv import load_dotenv
import os, csv, re
from pathlib import Path
from datetime import datetime

load_dotenv()
IS_PREMIUM_MODE = os.getenv("IS_PREMIUM_MODE", "false").lower() == "true"

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

OUTPUT_DIR = Path(os.path.join(BASE_DIR, "output")); OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR = Path(os.path.join(BASE_DIR, "uploads")); UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = os.path.join(BASE_DIR, "logs", "emails.csv"); os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def sanitize_filename(text: str) -> str:
    return re.sub(r"[^\w\-_.]", "_", text.strip()) or "AcePrep_Document"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/create-checkout-session")
async def stripe_checkout(request: Request):
    return create_checkout_session(request)

@app.get("/success")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/mock-checkout")
async def mock_checkout():
    return HTMLResponse("<h1>Mock Checkout</h1><p>Simulating payment...</p>")

@app.post("/generate")
async def generate(
    request: Request,
    job_link: str = Form(""),
    job_title: str = Form(""),
    job_description: str = Form(""),
    company_name: str = Form(""),
    job_role: str = Form(""),
    email: str = Form(""),
    resume_file: UploadFile = File(None)
):
    if IS_PREMIUM_MODE and not email.endswith("@test.com"):
        return templates.TemplateResponse("form.html", {"request": request, "error": "Premium access required."})

    if not email:
        return templates.TemplateResponse("form.html", {"request": request, "error": "Email is required."})

    if not job_link and not job_description:
        return templates.TemplateResponse("form.html", {"request": request, "error": "Job link or description is required."})

    # Extract job info from link
    job_data_raw = extract_job_description_from_url(job_link) if job_link else ""
    if isinstance(job_data_raw, dict):
        job_title = job_title or job_data_raw.get("job_title", "")
        job_description = job_description or job_data_raw.get("job_description", "")
    else:
        job_description = job_description or job_data_raw or "No description provided."

    # Resume context
    resume_context = {}
    resume_text = ""
    if resume_file:
        resume_path = UPLOAD_DIR / sanitize_filename(resume_file.filename)
        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())
        resume_context = extract_resume_context(str(resume_path))
        resume_text = resume_context.get("raw_text", "")
        job_title = job_title or resume_context.get("job_title", "")
        job_role = job_role or resume_context.get("job_role", "")
        company_name = company_name or resume_context.get("company_name", "")

    # === GPT + PDF Generation ===
    cheat_sheet_text = generate_cheat_sheet(resume_text, job_title, job_description, interviewer_type="Manager")

    filename = sanitize_filename(f"{job_title}_AcePrep.pdf")
    output_path = OUTPUT_DIR / filename

    export_cheat_sheet_pdf(
        user_name="",
        job_title=job_title,
        company_name=company_name,
        job_role=job_role,
        cheat_sheet_text=cheat_sheet_text,
        output_path=str(output_path)
    )

    if email:
        send_pdf_email(email, filename, str(output_path))
        with open("email_collector.csv", "a", encoding="utf-8") as collector:
            collector.write(email + "\n")
        with open(LOG_PATH, "a", newline="") as f:
            csv.writer(f).writerow([email, datetime.now().strftime("%Y-%m-%d %H:%M"), job_title])

    return FileResponse(output_path, media_type="application/pdf", filename=filename)
