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
    /* GLOBAL FRAMEWORK CANVAS SETUP */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F4F0E6 !important;
        color: #1E1E1C !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding: 2.5rem min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    
    /* --- ULTRACLEAN MATTE BLACK SIDEBAR ARCHITECTURE --- */
    [data-testid="stSidebar"] {
        background-color: #1E1E1C !important;
        border-right: none !important;
    }
    
    /* BRAND HEADINGS STYLE */
    .sidebar-logo {
        font-size: 24px;
        font-weight: 800;
        color: #E06A3B;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        padding: 1rem 0 2rem 0;
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

    /* PREMIUM FIELDS WITH SUBTLE SHADOWS */
    .stTextInput input, .stTextArea textarea, div[data-testid="stSelectbox"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D2C4 !important;
        border-radius: 6px !important;
        color: #1E1E1C !important;
        font-size: 14px !important;
        transition: all 0.2s ease-in-out;
    }

    /* Force specific pixel matching for text boxes */
    .stTextInput input {
        height: 43px !important;
        padding: 10px !important;
    }

    /* Force identical pixel box matching onto select box containers */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        height: 43px !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    div[data-baseweb="select"] > div:first-child {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        padding-left: 4px !important;
    }
    
    /* Active highlight focus transitions */
    .stTextInput input:focus, div[data-testid="stSelectbox"] > div:focus-within {
        border-color: #D35400 !important;
        box-shadow: 0 0 0 1px #D35400 !important;
    }
    
    /* Placeholder item text correction visibility */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #8C8A82 !important;
        opacity: 1 !important;
    }

    /* PREMIUM INTERACTIVE FLOATING SIDEBAR NAVIGATION BUTTONS */
    div[data-testid="stRadio"] > div {
        background-color: transparent !important;
        gap: 8px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        color: #A2A2A0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        text-transform: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* Clean removal of native choice indicator circles */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]::before,
    div[data-testid="stRadio"] div[data-testid="stWidgetWrapped-true"] {
        display: none !important;
    }
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    
    /* THE INDIVIDUAL COPPER ORANGE FLOATING ACTIVE SELECTION TILE */
    div[data-testid="stRadio"] div[data-checked="true"] label {
        background-color: #D35400 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(211, 84, 0, 0.2) !important;
    }
    
    div[data-testid="stRadio"] label:hover:not([data-checked="true"]) {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
    }

    /* MAIN BOTTOM FORM CONTROL INTERACTIONS */
    div.stButton > button:first-child {
        background-color: #D35400 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 2rem !important;
        transition: background-color 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #BA4A00 !important;
    }
    
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #1E1E1C !important;
        border: 1px solid #D6D2C4 !important;
    }
    div.stButton > button[key*="clear_btn"]:hover {
        background-color: #FAF8F5 !important;
    }
    
    /* INFRASTRUCTURE CONFIG BADGE BOTTOM FIXED CONTAINER */
    .status-badge {
        background-color: #162216;
        color: #52BE80;
        padding: 14px;
        border-radius: 6px;
        font-size: 12px;
        font-family: monospace;
        border: 1px solid #1F331F;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Panel Navigation Layer
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    
    # Custom rendering variables to cleanly inject dynamic counts into navigation fields
    scheduled_count = len(st.session_state.scheduled_emails)
    history_count = len(st.session_state.email_history)
    
    menu = st.radio(
        "Nav", 
        [
            "📝  Compose", 
            f"📅  Scheduled              ({scheduled_count})", 
            f"⏳  History                  ({history_count})"
        ], 
        label_visibility="collapsed"
    )
    st.markdown("<br>" * 12, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#2ECC71;">●</span> Gmail ready<br><b style="color:white; font-family:sans-serif; font-size:11px;">Configured</b></div>', unsafe_allow_html=True)

# --- PANEL BLOCK: COMPOSE LOOP ---
if "Compose" in menu:
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

    # 2. Status Output Messaging Cards
    if send_clicked:
        if to_field and subject_field and body_field:
            email_payload = {
                "to": to_field,
                "from": from_field,
                "subject": subject_field,
                "body": body_field,
                "timestamp": time_input_string
            }
            
            if "Schedule for later" in send_mode:
                st.session_state.scheduled_emails.append(email_payload)
                st.markdown("""
                    <div style="background-color: #EBF5FB; border-left: 5px solid #2980B9; padding: 15px; border-radius: 4px; margin-top: 20px;">
                        <b style="color: #1B4F72; font-size: 15px;">📅 Scheduled Successfully</b><br>
                        <span style="color: #2C3E50; font-size: 13px;">Outbound email successfully saved to your scheduled queue!</span>
                    </div>
                """, unsafe_allow_html=True)
                st.rerun()
            else:
                status_box = st.empty()
                status_box.markdown("""
                    <div style="background-color: #FEF9E7; border-left: 5px solid #F39C12; padding: 15px; border-radius: 4px; margin-top: 20px;">
                        <b style="color: #7D6608; font-size: 15px;">⏳ Sending email...</b><br>
                        <span style="color: #515A5A; font-size: 13px;">Accessing Google API cloud relays. Please wait...</span>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    send_email(to_field, subject_field, body_field)
                    st.session_state.email_history.append(email_payload)
                    
                    status_box.markdown("""
                        <div style="background-color: #E8F8F5; border-left: 5px solid #27AE60; padding: 15px; border-radius: 4px; margin-top: 20px;">
                            <b style="color: #117A65; font-size: 15px;">✅ Email sent successfully!</b><br>
                            <span style="color: #196F3D; font-size: 13px;">Dispatch confirmed. Message has left your Gmail account successfully.</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.toast("Email Dispatched!", icon="🚀")
                    st.rerun()
                    
                except Exception as e:
                    status_box.markdown(f"""
                        <div style="background-color: #FADBD8; border-left: 5px solid #CB4335; padding: 15px; border-radius: 4px; margin-top: 20px;">
                            <b style="color: #78281F; font-size: 15px;">❌ Delivery Failed</b><br>
                            <span style="color: #922B21; font-size: 13px;">Handshake Refused: {str(e)}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #FADBD8; border-left: 5px solid #CB4335; padding: 15px; border-radius: 4px; margin-top: 20px;">
                    <b style="color: #78281F; font-size: 15px;">⚠️ Validation Error</b><br>
                    <span style="color: #922B21; font-size: 13px;">Please make sure the TO, SUBJECT, and MESSAGE blocks are filled out.</span>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL BLOCK: SCHEDULED ---
elif "Scheduled" in menu:
    st.markdown('<div class="main-title">SCHEDULED EMAILS</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #5C5A55; font-size: 14px; margin-bottom: 15px;">Emails currently queued up for future automated delivery</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.scheduled_emails:
        st.info("No scheduled emails in your dispatch queue.")
    else:
        st.write(st.session_state.scheduled_emails)

# --- PANEL BLOCK: HISTORY ---
elif "History" in menu:
    st.markdown('<div class="main-title">TRANSMISSION HISTORY</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #5C5A55; font-size: 14px; margin-bottom: 15px;">Log of all successfully dispatched automated emails</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.email_history:
        st.info("No sent logs tracked yet.")
    else:
        st.write(st.session_state.email_history)
