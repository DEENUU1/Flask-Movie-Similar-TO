import os
import smtplib

from dotenv import load_dotenv
from flask import flash

load_dotenv()


def send_email(subject: str, message: str, to: str):
    """ This function allows to send emails
        It is using a standard python library called "smtplib" """
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            email_body = f"Subject: {subject}\n\n{message}"
            server.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(os.getenv("EMAIL_USERNAME"), to, email_body)
    except Exception as e:
        flash(f"An error accured while sending the email: {e}")
