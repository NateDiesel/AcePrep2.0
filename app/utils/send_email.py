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
