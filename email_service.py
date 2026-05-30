import base64
from email.mime.text import MIMEText
import streamlit as st

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def gmail_authenticate():

    config = {
        "web": {
            "client_id": st.secrets["gmail"]["client_id"],
            "client_secret": st.secrets["gmail"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = Flow.from_client_config(config, SCOPES)
    flow.redirect_uri = "http://localhost:8501"

    creds = flow.run_local_server(port=0)

    return build("gmail", "v1", credentials=creds)


def send_email(to, subject, body):
    service = gmail_authenticate()

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    message["from"] = "me"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    return "Email sent successfully"
