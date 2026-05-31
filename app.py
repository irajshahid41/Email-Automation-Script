import streamlit as st
import json
from datetime import datetime
# Import the secure service backend we set up earlier
from email_service import send_email

# 1. Initialize Global Session Tracking
if "scheduled_emails" not in st.session_state:
    st.session_state.scheduled_emails = []
if "email_history" not in st.session_state:
    st.session_state.email_history = []

# 2. Viewport Layout Matrix
st.set_page_config(page_title="MailFlow", page_icon="✉️", layout="wide")

# 3. Premium Retro/Modern Custom UI Theme
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F0E6 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container {
        padding: 3rem min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E1C !important;
    }
    .sidebar-logo {
        font-size: 24px;
        font-weight: 800;
        color: #E06A3B;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        padding: 1rem 0;
    }
    h1 {
        font-family: 'Impact', sans-serif !important;
        font-weight: 900 !important;
        color: #1E1E1C !important;
        font-size: 38px !important;
        margin-bottom: 0px !important;
    }
    label {
        color: #5C5A55 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 1px;
    }
    /* Input Field Overrides with Placeholders styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D2C4 !important;
        border-radius: 6px !important;
        color: #1E1E1C !important;
    }
    /* Combined Custom DateTime Input Styling matching your image */
    .custom-datetime-container input {
        width: 100%;
        background-color: #FFFFFF;
        border: 1px solid #D6D2C4;
        border-radius: 6px;
        padding: 10px;
        color: #1E1E1C;
        font-family: inherit;
        font-size: 14px;
    }
    /* Core Action Buttons */
    div.stButton > button:first-child {
        background-color: #D35400 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 1.8rem !important;
    }
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #1E1E1C !important;
        border: 1px solid #D6D2C4 !important;
    }
    .status-badge {
        background-color: #162216;
        color: #52BE80;
        padding: 12px;
        border-radius: 6px;
        font-size: 12px;
        font-family: monospace;
        margin-top: auto;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Navigation Control
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    menu = st.radio("Nav", ["📝 Compose", "📅 Scheduled", "⏳ History"], label_visibility="collapsed")
    st.markdown("<br>" * 12, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#2ECC71;">●</span> Gmail ready<br><b style="color:white;">Configured</b></div>', unsafe_allow_html=True)

# --- TAB VIEW: COMPOSE ---
if "Compose" in menu:
    st.markdown("<h1>NEW EMAIL</h1>", unsafe_allow_html=True)
    st.caption("Compose and schedule your email distribution loop")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        to_field = st.text_input("TO", placeholder="recipient@example.com")
    with col2:
        from_field = st.text_input("FROM (YOUR GMAIL)", placeholder="you@gmail.com")
        
    subject_field = st.text_input("SUBJECT", placeholder="Email subject line")
    body_field = st.st.text_area("MESSAGE", placeholder="Write your message here...", height=200)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<label>SCHEDULE DATE & TIME</label>", unsafe_allow_html=True)
        # Using a custom text component that saves data back securely to python
        time_input_string = st.text_input(
            "datetime_hidden_label", 
            value="2026-05-31 12:01 PM", 
            label_visibility="collapsed"
        )
    with col4:
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"])
        
    st.write("")
    
    # Execution Footers
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([6, 1, 1.2])
    with ctrl_col2:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.rerun()
            
    with ctrl_col3:
        if st.button("Send Email", key="send_btn", use_container_width=True):
            if to_field and subject_field and body_field:
                email_payload = {
                    "to": to_field,
                    "from": from_field,
                    "subject": subject_field,
                    "body": body_field,
                    "timestamp": time_input_string
                }
                
                if send_mode == "Schedule for later":
                    st.session_state.scheduled_emails.append(email_payload)
                    st.success("📅 Outbound email successfully saved to your scheduled queue!")
                else:
                    # 🔴 CRITICAL FIX FOR NOT SENDING:
                    # We wrap the transmission inside a clear feedback spinner to catch network faults
                    with st.spinner("Accessing Google API cloud relays..."):
                        try:
                            # Triggers the actual authentication engine from email_service.py
                            response = send_email(to_field, subject_field, body_field)
                            st.session_state.email_history.append(email_payload)
                            st.success("🚀 Dispatch confirmed! Message has left your Gmail account successfully.")
                        except Exception as e:
                            st.error(f"❌ Handshake Refused: {str(e)}")
                            st.info("Check your Streamlit Secrets panel to verify that your GCP_TOKEN hasn't been corrupted or misformatted.")
            else:
                st.error("⚠️ Validation Error: Please fill out TO, SUBJECT, and MESSAGE blocks.")
