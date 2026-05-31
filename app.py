import streamlit as st
import json
import time
from datetime import datetime
# Import your secured engine logic
from email_service import send_email

# 1. Initialize Application Trackers
if "scheduled_emails" not in st.session_state:
    st.session_state.scheduled_emails = []
if "email_history" not in st.session_state:
    st.session_state.email_history = []

st.set_page_config(page_title="MailFlow", page_icon="✉️", layout="wide")

# 2. Premium Overhaul Stylesheet Injection
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F0E6 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container {
        padding: 2.5rem min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E1C !important;
    }
    
    /* BRAND HEADINGS STYLE */
    .sidebar-logo {
        font-size: 24px;
        font-weight: 800;
        color: #E06A3B;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        padding: 1rem 0;
    }
    .main-title {
        font-family: 'Impact', sans-serif !important;
        font-weight: 900 !important;
        color: #1E1E1C !important;
        font-size: 38px !important;
        margin-bottom: 5px !important;
    }
    
    /* INPUT LABELS STYLE */
    label {
        color: #5C5A55 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 1px;
        margin-bottom: 6px !important;
    }

    /* INPUT FIELD DECORATION & PLACEHOLDER PATCH */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D2C4 !important;
        border-radius: 6px !important;
        color: #1E1E1C !important;
        font-size: 14px !important;
    }
    
    /* Forces placeholder text to be clearly visible */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #8C8A82 !important;
        opacity: 1 !important;
    }

    /* FORM ALIGNMENT CORRECTION */
    div[data-testid="stFormSubmitButton"] {
        text-align: right;
    }
    
    /* CORE ACTIONS INTERACTIVE OVERRIDES */
    div.stButton > button:first-child {
        background-color: #D35400 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 2rem !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #BA4A00 !important;
    }
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #1E1E1C !important;
        border: 1px solid #D6D2C4 !important;
    }
    
    /* BOTTOM CARD STATUS BADGE */
    .status-badge {
        background-color: #162216;
        color: #52BE80;
        padding: 12px;
        border-radius: 6px;
        font-size: 12px;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Panel Context
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    menu = st.radio("Nav", ["📝 Compose", "📅 Scheduled", "⏳ History"], label_visibility="collapsed")
    st.markdown("<br>" * 14, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#2ECC71;">●</span> Gmail ready<br><b style="color:white;">Configured</b></div>', unsafe_allow_html=True)

# --- PANEL BLOCK: COMPOSE LOOP ---
if "Compose" in menu:
    #  NEW VISIBLE LINES:
    st.markdown('<div class="main-title">NEW EMAIL</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #5C5A55; font-size: 14px; margin-bottom: 15px;">Compose and schedule your email distribution loop</div>', unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        to_field = st.text_input("TO", placeholder="recipient@example.com")
    with col2:
        from_field = st.text_input("FROM (YOUR GMAIL)", placeholder="you@gmail.com")
        
    subject_field = st.text_input("SUBJECT", placeholder="Email subject line")
    body_field = st.text_area("MESSAGE", placeholder="Write your message here...", height=200)
    
    # Precise Alignment row for Scheduling Elements
    col3, col4 = st.columns(2)
    with col3:
        time_input_string = st.text_input("SCHEDULE DATE & TIME", value="2026-05-31 12:01 PM")
    with col4:
        # Added an empty string as a label to perfectly sync the alignment baseline with the text box
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"])
        
    st.write("")
    
    # Interaction Control Footers
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
                    # 🚀 INTERACTIVE LIVE PROGRESS UPDATER BLOCK
                    with st.status("⏳ Sending email...", expanded=True) as status:
                        try:
                            # Deliver via our authenticated Gmail API script connection
                            send_email(to_field, subject_field, body_field)
                            
                            # Log record to Session State history
                            st.session_state.email_history.append(email_payload)
                            
                            # Update statuses cleanly when successfully delivered
                            status.update(label="✅ Email sent successfully!", state="complete", expanded=False)
                            st.toast("Email Dispatched!", icon="🚀")
                        except Exception as e:
                            status.update(label="❌ Delivery Failed", state="error", expanded=True)
                            st.error(f"Handshake Refused: {str(e)}")
            else:
                st.error("⚠️ Validation Error: Please fill out TO, SUBJECT, and MESSAGE blocks.")

# --- PANEL BLOCK: SCHEDULED ---
elif "Scheduled" in menu:
    st.markdown('<div class="main-title">SCHEDULED EMAILS</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.scheduled_emails:
        st.info("No scheduled emails in your dispatch queue.")
    else:
        st.write(st.session_state.scheduled_emails)

# --- PANEL BLOCK: HISTORY ---
elif "History" in menu:
    st.markdown('<div class="main-title">TRANSMISSION HISTORY</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.email_history:
        st.info("No sent logs tracked yet.")
    else:
        st.write(st.session_state.email_history)
