from app.utils.openrouter import chat_completion

def generate_cheat_sheet(resume_text=None, job_title=None, job_description=None, interviewer_type="Manager"):
    if not resume_text and not job_description:
        raise ValueError("❌ Need at least resume text or job description.")

    if job_title and job_description and resume_text:
        prompt = f"""
You are an expert interview coach. Based on this job and resume, generate a tailored interview prep pack.

Job Title: {job_title}
Job Description:
{job_description}

Resume:
{resume_text}

Instructions:
1. Generate 15–20 tailored interview questions
2. Generate 5–10 crossover questions based on the resume
3. Provide 3–5 smart questions to ask the interviewer ({interviewer_type})

Label each section:
- Top Interview Questions (Tailored)
- Resume-Based Crossover Questions
- Questions to Ask the Interviewer ({interviewer_type})
"""
    elif job_description:
        prompt = f"""
You are an expert interview coach. Based on this job description, generate interview questions.

Job Description:
{job_description}

Instructions:
1. Generate 15–20 questions they might be asked
2. Provide 3–5 questions to ask the interviewer ({interviewer_type})
"""
    elif resume_text:
        prompt = f"""
You are an expert interview coach. Based on this resume, generate general interview prep.

Resume:
{resume_text}

Instructions:
1. Generate 15–20 general interview questions
2. Provide 3–5 questions to ask the interviewer ({interviewer_type})
"""
    else:
        raise ValueError("❌ Insufficient input to generate cheat sheet.")

    return chat_completion(prompt)
