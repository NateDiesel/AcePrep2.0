from app.utils.openrouter import chat_completion  # ✅ Using OpenRouter

def generate_cheat_sheet(resume_text, job_title, job_description, interviewer_type="Manager"):
    if not all([resume_text, job_title, job_description]):
        raise ValueError("❌ Missing required context for OpenRouter prompt.")

    prompt = f"""
You are an expert technical interview coach. Based on the following details, generate a full interview prep pack.

Job Title: {job_title}

Job Description:
{job_description}

Resume Content:
{resume_text}

Instructions:
1. Generate 15–20 tailored interview questions for this role.
2. Generate 5–10 crossover questions based on the resume.
3. Provide 3–5 smart questions to ask the interviewer ({interviewer_type}).

Label each section:
- Top Interview Questions (Tailored)
- Resume-Based Crossover Questions
- Questions to Ask the Interviewer ({interviewer_type})
"""
    return chat_completion(prompt)
