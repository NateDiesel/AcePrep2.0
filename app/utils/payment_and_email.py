
import os
import sendgrid
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "contact@content365.xyz"
FROM_NAME = "Nathan Bentley"

def send_pdf_email(to_email, filename, filepath):
    if not SENDGRID_API_KEY:
        print("SendGrid API key missing.")
        return

    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject="🎯 Your AcePrep Interview Cheat Sheet",
        html_content=f"Hi there,<br><br>Attached is your personalized interview prep PDF.<br><br>Good luck!<br><br>-AcePrep Team",
    )

    with open(filepath, "rb") as f:
        data = f.read()
        import base64
        encoded = base64.b64encode(data).decode()
        message.add_attachment({
            'file_content': encoded,
            'file_type': 'application/pdf',
            'file_name': filename,
            'disposition': 'attachment'
        })

    try:
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent:", response.status_code)
    except Exception as e:
        print("Email error:", str(e))
