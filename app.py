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

# 2. Premium Overhaul Stylesheet Injection (Nordic Tech & Slate Theme)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F9F9F7 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding: 3rem min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    
    /* SIDEBAR MATTE OBSIDIAN COLOR */
    [data-testid="stSidebar"] {
        background-color: #1A2222 !important;
    }
    
    /* BRAND HEADINGS STYLE */
    .sidebar-logo {
        font-size: 24px;
        font-weight: 800;
        color: #C05621;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 3px;
        padding: 1rem 0;
    }
    .main-title {
        font-family: 'Impact', sans-serif !important;
        font-weight: 900 !important;
        color: #2D3748 !important;
        font-size: 38px !important;
        margin-bottom: 5px !important;
        letter-spacing: 0.5px;
    }
    
    /* INPUT LABELS STYLE */
    label {
        color: #718096 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 1.5px;
        margin-bottom: 8px !important;
    }

    /* PREMIUM FIELDS WITH SUBTLE SHADOWS */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #1A202C !important;
        font-size: 14px !important;
        padding: 10px !important;
        transition: all 0.2s ease-in-out;
    }
    
    /* Crisp focus highlight */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #C05621 !important;
        box-shadow: 0 0 0 1px #C05621 !important;
    }
    
    /* Clear placeholder visibility */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #A0AEC0 !important;
        opacity: 1 !important;
    }

    /* FORM ALIGNMENT CORRECTION */
    div[data-testid="stFormSubmitButton"] {
        text-align: right;
    }
    
    /* MATTE COPPER ORANGE BUTTON ACTION */
    div.stButton > button:first-child {
        background-color: #C05621 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        padding: 0.6rem 2.2rem !important;
        box-shadow: 0 2px 4px rgba(192, 86, 33, 0.15);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #9C4216 !important;
        box-shadow: 0 4px 8px rgba(192, 86, 33, 0.25);
    }
    
    /* Secondary Clear Button */
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #4A5568 !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    div.stButton > button[key*="clear_btn"]:hover {
        background-color: #F7FAFC !important;
        color: #1A202C !important;
    }
    
    /* COMPACT CONFIGURATION FOOTER CARD */
    .status-badge {
        background-color: #232E2E;
        color: #48BB78;
        padding: 14px;
        border-radius: 8px;
        font-size: 12px;
        font-family: monospace;
        border: 1px solid #2B3A3A;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Panel Context
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    menu = st.radio("Nav", ["📝 Compose", "📅 Scheduled", "⏳ History"], label_visibility="collapsed")
    st.markdown("<br>" * 14, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#48BB78;">●</span> Gmail ready<br><b style="color:white;">Configured</b></div>', unsafe_allow_html=True)

# --- PANEL BLOCK: COMPOSE LOOP ---
if "Compose" in menu:
    st.markdown('<div class="main-title">NEW EMAIL</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #718096; font-size: 14px; margin-bottom: 20px;">Compose and schedule your email distribution loop</div>', unsafe_allow_html=True)
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
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"])
        
    st.write("")
    
    # 1. Interaction Control Footers Row
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([6, 1, 1.2])
    with ctrl_col2:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.rerun()
            
    with ctrl_col3:
        send_clicked = st.button("Send Email", key="send_btn", use_container_width=True)

    # 2. Dedicated Status Row (Appears perfectly below the buttons)
    if send_clicked:
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
                st.markdown("""
                    <div style="background-color: #EBF8FF; border-left: 5px solid #3182CE; padding: 15px; border-radius: 6px; margin-top: 20px;">
                        <b style="color: #2B6CB0; font-size: 15px;">📅 Scheduled Successfully</b><br>
                        <span style="color: #4A5568; font-size: 13px;">Outbound email successfully saved to your scheduled queue!</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Placeholder for the active state
                status_box = st.empty()
                status_box.markdown("""
                    <div style="background-color: #FFFDF5; border-left: 5px solid #D69E2E; padding: 15px; border-radius: 6px; margin-top: 20px;">
                        <b style="color: #975A16; font-size: 15px;">⏳ Sending email...</b><br>
                        <span style="color: #718096; font-size: 13px;">Accessing Google API cloud relays. Please wait...</span>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    # Deliver via our authenticated Gmail API script connection
                    send_email(to_field, subject_field, body_field)
                    
                    # Log record to Session State history
                    st.session_state.email_history.append(email_payload)
                    
                    # Overwrite placeholder with a highly visible custom Success Highlight Row
                    status_box.markdown("""
                        <div style="background-color: #F0FFF4; border-left: 5px solid #38A169; padding: 15px; border-radius: 6px; margin-top: 20px;">
                            <b style="color: #276749; font-size: 15px;">✅ Email sent successfully!</b><br>
                            <span style="color: #2F855A; font-size: 13px;">Dispatch confirmed. Message has left your Gmail account successfully.</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.toast("Email Dispatched!", icon="🚀")
                    
                except Exception as e:
                    status_box.markdown(f"""
                        <div style="background-color: #FFF5F5; border-left: 5px solid #E53E3E; padding: 15px; border-radius: 6px; margin-top: 20px;">
                            <b style="color: #9B2C2C; font-size: 15px;">❌ Delivery Failed</b><br>
                            <span style="color: #C53030; font-size: 13px;">Handshake Refused: {str(e)}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #FFF5F5; border-left: 5px solid #E53E3E; padding: 15px; border-radius: 6px; margin-top: 20px;">
                    <b style="color: #9B2C2C; font-size: 15px;">⚠️ Validation Error</b><br>
                    <span style="color: #C53030; font-size: 13px;">Please make sure the TO, SUBJECT, and MESSAGE blocks are filled out.</span>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL BLOCK: SCHEDULED ---
elif "Scheduled" in menu:
    st.markdown('<div class="main-title">SCHEDULED EMAILS</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #718096; font-size: 14px; margin-bottom: 20px;">Emails currently queued up for future automated delivery</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.scheduled_emails:
        st.markdown('<div style="text-align: center; padding: 5rem 2rem; color: #A0AEC0; font-family: monospace; font-size: 16px;">📅 No scheduled emails in your dispatch queue.</div>', unsafe_allow_html=True)
    else:
        st.write(st.session_state.scheduled_emails)

# --- PANEL BLOCK: HISTORY ---
elif "History" in menu:
    st.markdown('<div class="main-title">TRANSMISSION HISTORY</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #718096; font-size: 14px; margin-bottom: 20px;">Log of all successfully dispatched automated emails</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.email_history:
        st.markdown('<div style="text-align: center; padding: 5rem 2rem; color: #A0AEC0; font-family: monospace; font-size: 16px;">⏳ No tracked sent logs available yet.</div>', unsafe_allow_html=True)
    else:
        st.write(st.session_state.email_history)
