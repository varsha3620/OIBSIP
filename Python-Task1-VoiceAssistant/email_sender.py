import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(recipient, subject, message):

    email = MIMEText(message)

    email["Subject"] = subject
    email["From"] = EMAIL_ADDRESS
    email["To"] = recipient

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(email)

        return True

    except Exception as e:

        print("Email error:", e)

        return False
