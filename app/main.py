
from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime

from app.utils.parser import extract_resume_context, extract_job_description_from_url
from app.utils.generate_cheat_sheet import generate_cheat_sheet
from app.utils.pdf_generator import export_cheat_sheet_pdf
from app.utils.payment_and_email import send_pdf_email
from app.utils.stripe_checkout import create_checkout_session

load_dotenv()
IS_PREMIUM_MODE = os.getenv("IS_PREMIUM_MODE", "false").lower() == "true"

app = FastAPI(title="AcePrep – Interview Cheat Sheet")
BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR.parent / "static"   # static is alongside /app
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

OUTPUT_DIR = BASE_DIR / "output"
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "premium": IS_PREMIUM_MODE})

@app.get("/form", response_class=HTMLResponse)
async def form_get(request: Request, error: str | None = None):
    return templates.TemplateResponse("form.html", {"request": request, "error": error, "premium": IS_PREMIUM_MODE})

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    job_link: str | None = Form(None),
    job_title: str | None = Form(None),
    company_name: str | None = Form(None),
    role: str | None = Form(None),
    name: str | None = Form(None),
    email: str | None = Form(None),
    resume: UploadFile | None = File(None)
):
    resume_path = None
    resume_text = None
    if resume and resume.filename:
        suffix = Path(resume.filename).suffix.lower()
        if suffix in [".pdf", ".docx"]:
            resume_path = UPLOAD_DIR / f"{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}{suffix}"
            data = await resume.read()
            resume_path.write_bytes(data)
            resume_text = extract_resume_context(str(resume_path))
        else:
            return templates.TemplateResponse("form.html", {"request": request, "error": "Please upload a PDF or DOCX."})

    job_description = None
    if job_link:
        job_description = extract_job_description_from_url(job_link)

    pack = generate_cheat_sheet(
        resume_text=resume_text or "",
        job_title=job_title or "",
        job_description=job_description or "",
        interviewer_type=role or "Manager",
    )

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    out_path = OUTPUT_DIR / f"aceprep_{ts}.pdf"
    export_cheat_sheet_pdf(
        job_title=job_title or "",
        job_description=pack.get("summary", job_description or ""),
        job_role=role or "",
        company_name=company_name or "",
        user_name=name or "",
        questions_top=pack.get("questions_top", []),
        questions_resume=pack.get("questions_resume", []),
        questions_to_ask=pack.get("questions_to_ask", []),
        output_path=str(out_path),
    )

    if email:
        try:
            send_pdf_email(email, "Your AcePrep Interview Cheat Sheet", str(out_path))
        except Exception as e:
            print("Email failed:", e)

    return templates.TemplateResponse(
        "generate.html",
        {
            "request": request,
            "pdf_path": f"/download/{out_path.name}",
            "email": email,
            "premium": IS_PREMIUM_MODE,
        },
    )

@app.get("/download/{filename}")
async def download(filename: str):
    path = OUTPUT_DIR / filename
    return FileResponse(path, filename=filename, media_type="application/pdf")

@app.get("/buy")
async def buy(request: Request):
    if not IS_PREMIUM_MODE:
        return RedirectResponse(url="/form")
    session = create_checkout_session(request)
    return RedirectResponse(session.url)

@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})
