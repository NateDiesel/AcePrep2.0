# AcePrep – Interview Cheat Sheet (FastAPI)

Tailored interview prep in seconds: upload your resume, paste a job link, and get a clean PDF with **role summary**, **tailored interview questions**, **resume-based crossover questions**, and **smart questions to ask**.

<p align="center">
  <img alt="AcePrep" src="https://img.shields.io/badge/FastAPI-🚀-brightgreen"> 
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue">
  <img alt="ReportLab" src="https://img.shields.io/badge/PDF-ReportLab-informational">
  <img alt="OpenRouter" src="https://img.shields.io/badge/LLM-OpenRouter-9cf">
</p>

## ✨ Features
- **Resume upload** (PDF/DOCX) parsing
- **Job link parsing** to pull the description
- **LLM-tailored content** with safe fallback (works without API keys)
- **Branded PDF export**
- **Optional email delivery** via SendGrid
- **Stripe checkout hooks** (disabled by default)
- Dockerfile + Railway friendly

## 🧪 Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # add keys later if desired
uvicorn app.main:app --reload
# open http://127.0.0.1:8000
```

## 🔐 Environment
```env
IS_PREMIUM_MODE=false
OPENROUTER_API_KEY=
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
SENDGRID_API_KEY=
FROM_EMAIL=contact@content365.xyz
FROM_NAME=AcePrep
STRIPE_SECRET_KEY=
STRIPE_PRICE_ID=
```

> No keys? No problem — the app still runs and produces a solid PDF using the built-in **fallback**.

## 🖼️ Screenshots & Sample
- `docs/screenshot-form.png` (add)
- `docs/screenshot-result.png` (add)
- `sample_output/aceprep-sample.pdf` (generated)

## 🧠 What this demonstrates
- FastAPI routing, forms, file uploads
- Resume & job-link parsing (pdfplumber, python-docx, bs4)
- LLM prompt design + robust fallback
- PDF generation with ReportLab
- Optional email (SendGrid) and Stripe hooks
- Containerized deploy (Docker)

## 🚀 Deploy (Docker)
```bash
docker build -t aceprep .
docker run -p 8000:8000 --env-file .env aceprep
```

## 📬 Contact
**Nathan Bentley** · contact@content365.xyz · GitHub: @NateDiesel
