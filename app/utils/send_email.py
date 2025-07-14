<<<<<<< HEAD

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Attachment, FileContent, FileName, FileType, Disposition
import base64

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "contact@content365.xyz")

def send_pdf_email(to_email, filename, filepath):
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        raise EnvironmentError("Missing SENDGRID_API_KEY or FROM_EMAIL")

    with open(filepath, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode()

    message = Mail(
        from_email=Email(FROM_EMAIL, name="AcePrep"),
        to_emails=To(to_email),
        subject=f"Your AcePrep Interview Cheat Sheet: {filename}",
        html_content="Your interview prep PDF is attached. Good luck!"
    )

    attachment = Attachment(
        FileContent(encoded_file),
        FileName(filename),
        FileType("application/pdf"),
        Disposition("attachment")
    )

    message.attachment = attachment

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print("✅ Email sent:", response.status_code)
=======
import os
import base64
import requests

def send_pdf_email(to_email: str, subject: str, html: str, attachment_path: str = None):
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        raise ValueError("SENDGRID_API_KEY is not set in the environment.")

    from_email = "contact@content365.xyz"
    from_name = "Nathan Bentley"
    reply_to = {"email": "contact@content365.xyz"}

    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {
            "email": from_email,
            "name": from_name
        },
        "reply_to": reply_to,
        "content": [
            {
                "type": "text/html",
                "value": html
            }
        ]
    }

    if attachment_path:
        with open(attachment_path, "rb") as f:
            encoded_file = base64.b64encode(f.read()).decode()
            data["attachments"] = [
                {
                    "content": encoded_file,
                    "type": "application/pdf",
                    "filename": os.path.basename(attachment_path),
                    "disposition": "attachment"
                }
            ]

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )

    if response.status_code >= 400:
        raise RuntimeError(f"Failed to send email: {response.status_code} - {response.text}")
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)
