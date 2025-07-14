import requests
from bs4 import BeautifulSoup

def extract_job_description_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try LinkedIn-style div or general job-post sections
        possible_selectors = [
            {"name": "div", "attrs": {"class": lambda c: c and "description" in c}},
            {"name": "section"},
            {"name": "article"},
        ]

        text_blocks = []
        for sel in possible_selectors:
            for tag in soup.find_all(sel["name"], attrs=sel.get("attrs")):
                text = tag.get_text(separator=" ", strip=True)
                if text and len(text.split()) > 50:
                    text_blocks.append(text)

        full_text = " ".join(text_blocks)
        junk_phrases = ["Join now", "LinkedIn", "Cookie", "Privacy Policy", "User Agreement"]
        for junk in junk_phrases:
            full_text = full_text.replace(junk, "")

        return full_text.strip()
    except Exception as e:
        return f"Job description extraction failed: {e}"