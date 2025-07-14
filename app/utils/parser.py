
import docx
import pdfplumber
import re
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or '' for page in pdf.pages)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_resume_context(file_path):
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file type."

    # Extract basic keywords
    skills = re.findall(r"(?i)(skills|technologies):?\s*(.*)", raw_text)
    experience = re.findall(r"(?i)(experience|roles):?\s*(.*)", raw_text)
    return {
        "raw_text": raw_text[:3000],  # Trim for GPT input
        "skills": skills,
        "experience": experience
    }

def extract_job_description_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join(p.get_text(strip=True) for p in paragraphs)[:3000]
    except Exception as e:
        return f"Failed to parse job link: {str(e)}"
