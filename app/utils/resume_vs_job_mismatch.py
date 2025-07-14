import re

def detect_resume_job_mismatch(resume_text, job_title, job_description):
    healthcare_keywords = ["nurse", "CNA", "LPN", "patient", "clinic", "hospital", "healthcare", "RN"]
    tech_keywords = ["developer", "engineer", "backend", "API", "python", "fastapi", "software"]

    resume_lower = resume_text.lower()
    job_combined = f"{job_title}\n{job_description}".lower()

    healthcare_count = sum(kw in resume_lower for kw in healthcare_keywords)
    tech_count = sum(kw in job_combined for kw in tech_keywords)

    if healthcare_count > 3 and tech_count > 3:
        return (
            "⚠️ Your resume appears to focus on **healthcare**, "
            "while this job is for a **software developer**. "
            "You may want to upload a more relevant resume."
        )
    return None