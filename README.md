# 🧠 AcePrep™ – AI-Powered Interview Cheat Sheet Generator

AcePrep™ is a production-grade FastAPI app that helps job seekers prepare for interviews by generating tailored, AI-powered cheat sheets — complete with recruiter-style questions, personalized context, and branded PDF export.

---

## 🚀 Features

✅ Upload your resume (PDF/DOCX)  
✅ Paste a job description or job link  
✅ Get 20 tailored interview questions  
✅ Includes suggested questions to ask HR, managers, and CEOs  
✅ Branded PDF export with smart layout  
✅ Email delivery via SendGrid  
✅ Stripe-ready mock checkout page  
✅ Fully Dockerized and deployable on Railway

---

## 📸 Screenshots

> _Coming soon! Add screenshots for `/`, `/generate`, and the PDF preview_

---

## 🛠 Tech Stack

- **Python 3.10+**
- **FastAPI + Jinja2**
- **SendGrid API** (email delivery)
- **Together.ai** (LLM-powered question generation)
- **FPDF** (PDF generation)
- **Docker** (for deployment)
- **Railway** (hosting)

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/NateDiesel/AcePrep2.0.git
cd AcePrep2.0

python -m venv venv
# Activate the virtual environment:
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload --port 8000
