import os
import base64
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def gmail_authenticate():
    creds = None

    # Load saved token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 🔴 FIX: ensures file is found in project root
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console and place it in the project folder."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

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
