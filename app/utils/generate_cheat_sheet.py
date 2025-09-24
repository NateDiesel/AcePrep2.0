
from app.utils.openrouter import chat_completion

FALLBACK = {
    "summary": "Role overview and key responsibilities summarized here.",
    "questions_top": [
        "Tell me about a challenging project and your role.",
        "How do you prioritize tasks with conflicting deadlines?",
        "Describe a time you improved a process end-to-end.",
    ],
    "questions_resume": [
        "Walk me through how your past experience maps to this role.",
        "Which achievement best demonstrates the skills we need here?",
    ],
    "questions_to_ask": [
        "What does success in the first 90 days look like?",
        "How does this team measure impact?",
    ],
}

def parse_sections(text: str) -> dict:
    out = {"summary": "", "questions_top": [], "questions_resume": [], "questions_to_ask": []}
    lines = [l.strip() for l in text.splitlines()]
    bucket = None
    for line in lines:
        header = line.lower()
        if "top interview questions" in header:
            bucket = "questions_top"; continue
        if "resume-based" in header or "crossover" in header:
            bucket = "questions_resume"; continue
        if "questions to ask" in header:
            bucket = "questions_to_ask"; continue
        if bucket and line:
            if line.startswith("-"):
                out[bucket].append(line.lstrip("- ").strip())
            else:
                out[bucket].append(line)
        elif not bucket:
            out["summary"] += (line + " ")
    out["summary"] = out["summary"].strip()
    return out

def generate_cheat_sheet(resume_text=None, job_title=None, job_description=None, interviewer_type="Manager"):
    if not (resume_text or job_description):
        return FALLBACK

    prompt = f"""
You are a senior interview coach. Using the job info and resume, produce:
1) A brief role summary (2–3 sentences).
2) "Top Interview Questions (Tailored)" — 12–15 bullets.
3) "Resume-Based Crossover Questions" — 5–8 bullets.
4) "Questions to Ask the Interviewer ({interviewer_type})" — 5–8 bullets.
Format with clear section headers and dash bullets.

Job Title: {job_title or 'N/A'}

Job Description:
{job_description or 'N/A'}

Resume:
{resume_text or 'N/A'}
"""

    try:
        content = chat_completion(prompt)
        parsed = parse_sections(content)
        for k, v in list(parsed.items()):
            if isinstance(v, list) and not v:
                parsed[k] = FALLBACK.get(k, v)
        if not parsed.get("summary"):
            parsed["summary"] = FALLBACK["summary"]
        return parsed
    except Exception:
        return FALLBACK
