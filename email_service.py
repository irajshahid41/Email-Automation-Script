import os
import base64
import json
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import streamlit as st

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None

    # 1. Try to load token from Streamlit Secrets first (Best for Cloud)
    if "GCP_TOKEN" in st.secrets:
        token_info = json.loads(st.secrets["GCP_TOKEN"])
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    
    # 2. Fallback to local pickle file for local development
    elif os.path.exists("token.pickle"):
        import pickle
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # 3. If credentials are expired, refresh them automatically
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    # 4. If absolutely no credentials exist
    if not creds:
        # If running locally, you can fallback to the client secret file flow
        if os.path.exists("credentials.json"):
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            raise FileNotFoundError(
                "No valid authentication found. Please configure Streamlit Secrets or provide credentials.json locally."
            )

    return build("gmail", "v1", credentials=creds)

def send_email(to, subject, body):
    service = gmail_authenticate()

    # Create email
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    # Encode email
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {"raw": raw_message}

    # Send email
    result = service.users().messages().send(
        userId="me",
        body=send_message
    ).execute()

    return result
