
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64

FROM_EMAIL = os.getenv("FROM_EMAIL", "contact@content365.xyz")
FROM_NAME = os.getenv("FROM_NAME", "AcePrep")

def send_pdf_email(to_email: str, subject: str, attachment_path: str):
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        print("SendGrid disabled (no SENDGRID_API_KEY).")
        return
    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject=subject,
        html_content="Your personalized cheat sheet is attached."
    )
    with open(attachment_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    message.add_attachment({
        "content": encoded,
        "type": "application/pdf",
        "filename": os.path.basename(attachment_path),
        "disposition": "attachment"
    })
    sg = SendGridAPIClient(api_key)
    sg.send(message)
