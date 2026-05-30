import streamlit as st
import time
import threading
from datetime import datetime

from email_service import send_email

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Email Automation UI", layout="wide")

# ---------------- SESSION STATE ----------------
if "logs" not in st.session_state:
    st.session_state.logs = []

if "running" not in st.session_state:
    st.session_state.running = False


# ---------------- BACKGROUND SCHEDULER ----------------
def scheduler_loop(interval, to, subject, body):
    while st.session_state.running:
        result = send_email(to, subject, body)
        st.session_state.logs.append(f"{datetime.now()} | {result} → {to}")
        time.sleep(interval)


# ---------------- UI ----------------
st.title("📧 Email Automation Dashboard")

col1, col2 = st.columns(2)

with col1:
    to = st.text_input("Receiver Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")

with col2:
    interval = st.number_input("Interval (seconds)", min_value=10, value=60)


# ---------------- BUTTONS ----------------
col3, col4, col5 = st.columns(3)

with col3:
    if st.button("📤 Send Now"):
        result = send_email(to, subject, body)
        st.session_state.logs.append(f"{datetime.now()} | {result}")
        st.success(result)

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
            st.success("Scheduler started")

with col5:
    if st.button("⛔ Stop Scheduler"):
        st.session_state.running = False
        st.warning("Scheduler stopped")


# ---------------- LOGS ----------------
st.divider()
st.subheader("📊 Activity Log")

for log in reversed(st.session_state.logs[-15:]):
    st.write(log)
