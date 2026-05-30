import streamlit as st
import time
import threading
from datetime import datetime

from email.mime.text import MIMEText
import base64
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# ---------------- CONFIG ----------------
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

st.set_page_config(page_title="Email Automation UI", layout="wide")

# ---------------- SESSION STATE ----------------
if "logs" not in st.session_state:
    st.session_state.logs = []

if "running" not in st.session_state:
    st.session_state.running = False


# ---------------- GMAIL AUTH ----------------
def gmail_authenticate():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


# ---------------- SEND EMAIL ----------------
def send_email(to, subject, body):
    service = gmail_authenticate()

    message = MIMEText(body)
    message["to"] = to
    message["from"] = "me"
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()

        log = f"✅ {datetime.now()} | Sent to {to}"
        st.session_state.logs.append(log)

    except Exception as e:
        st.session_state.logs.append(f"❌ Error: {e}")


# ---------------- BACKGROUND SCHEDULER ----------------
def scheduler_loop(interval, to, subject, body):
    while st.session_state.running:
        send_email(to, subject, body)
        time.sleep(interval)


# ---------------- UI ----------------
st.title("📧 Email Automation Dashboard")
st.caption("Control Gmail automation from a clean UI")

col1, col2 = st.columns(2)

with col1:
    to = st.text_input("📨 Receiver Email", "example@gmail.com")
    subject = st.text_input("📌 Subject", "Hello from UI")
    body = st.text_area("✉️ Message", "This is an automated email")

with col2:
    interval = st.number_input("⏱ Interval (seconds)", min_value=10, value=60)

# ---------------- BUTTONS ----------------
col3, col4, col5 = st.columns(3)

with col3:
    if st.button("📤 Send Now"):
        send_email(to, subject, body)
        st.success("Email sent!")

with col4:
    if st.button("▶️ Start Scheduler"):
        if not st.session_state.running:
            st.session_state.running = True
            thread = threading.Thread(
                target=scheduler_loop,
                args=(interval, to, subject, body),
                daemon=True
            )
            thread.start()
            st.success("Scheduler started!")

with col5:
    if st.button("⛔ Stop Scheduler"):
        st.session_state.running = False
        st.warning("Scheduler stopped!")

# ---------------- LOG PANEL ----------------
st.divider()
st.subheader("📊 Email Activity Log")

for log in reversed(st.session_state.logs[-10:]):
    st.write(log)