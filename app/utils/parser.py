
import requests, pdfplumber
from bs4 import BeautifulSoup
from docx import Document

def extract_text_from_pdf(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)

def extract_text_from_docx(path: str) -> str:
    d = Document(path)
    return "\n".join(p.text for p in d.paragraphs)

def extract_resume_context(path: str) -> str:
    try:
        if path.lower().endswith(".pdf"):
            return extract_text_from_pdf(path)
        if path.lower().endswith(".docx"):
            return extract_text_from_docx(path)
        return "Unsupported file type."
    except Exception as e:
        return f"Error reading resume: {e}"

def extract_job_description_from_url(url: str) -> str:
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12).text
        soup = BeautifulSoup(html, "html.parser")
        candidates = []
        for tag in soup.find_all(["section","article","div","main"]):
            text = tag.get_text(" ", strip=True)
            if text and len(text.split()) > 80:
                candidates.append(text)
        candidates.sort(key=len, reverse=True)
        return candidates[0][:5000] if candidates else "Could not extract job description."
    except Exception as e:
        return f"Job link fetch error: {e}"
