import os
import smtplib
from email.message import EmailMessage

from config import SENDER_EMAIL, APP_PASSWORD


def send_email(recipients, subject, content, attachments=None, plots=None):
    if not SENDER_EMAIL:
        raise ValueError("SENDER_EMAIL is not set.")
    if not APP_PASSWORD:
        raise ValueError("APP_PASSWORD is not set.")

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.add_alternative(content, subtype="html")

    files = []
    if attachments:
        files.extend(attachments)
    if plots:
        files.extend(plots)

    for file_path in files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Attachment not found: {file_path}")

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(file_path)
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
