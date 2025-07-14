<<<<<<< HEAD
import re
from app.utils.together import chat_completion

def generate_cheat_sheet(resume_text, job_title, job_description, interviewer_type="Manager"):
    # 🛡️ Defensive checks
    if not all([resume_text, job_title, job_description]):
        raise ValueError("❌ Missing required context for Together.ai prompt.")

=======
from app.utils.together import chat_completion

def generate_cheat_sheet(resume_text, job_title, job_description, interviewer_type="Manager"):
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)
    prompt = f"""
You are an expert technical interview coach. Based on the following details, generate a full interview prep pack.

Job Title: {job_title}

Job Description:
{job_description}

Resume Content:
{resume_text}

Instructions:
<<<<<<< HEAD
1. Generate 15–20 tailored interview questions for this role.
2. Generate 5–10 crossover questions based on the resume.
3. Provide 3–5 smart questions to ask the interviewer ({interviewer_type}).
=======
1. Generate 15–20 tailored interview questions specifically for this role.
2. Generate 5–10 questions that connect the resume background to the job (e.g., from healthcare to tech).
3. Based on the interviewer type ({interviewer_type}), generate 3–5 smart questions the candidate can ask the interviewer.
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)

Label each section:
- Top Interview Questions (Tailored)
- Resume-Based Crossover Questions
- Questions to Ask the Interviewer ({interviewer_type})
"""
<<<<<<< HEAD

    print("🔍 Prompt preview (first 200 chars):\n", prompt[:200], "...\n")
    return chat_completion(prompt)
=======
    return chat_completion(prompt)
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)
