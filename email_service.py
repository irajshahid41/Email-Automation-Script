import smtplib
import streamlit as st
from email.mime.text import MIMEText


def send_email(to, subject, body):
    sender = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        return "✅ Email sent successfully"

    except Exception as e:
        return f"❌ Error: {e}"
