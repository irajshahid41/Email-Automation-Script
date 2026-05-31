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

# 2. Cyber Obsidian & Neon Overhaul Stylesheet Injection
st.markdown("""
    <style>
    /* GLOBAL DARK MODE SETUP */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #12141C !important;
        color: #F7FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding: 3rem min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    
    /* --- NEW PROFESSIONAL SIDEBAR ARCHITECTURE --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #151821 0%, #0E1017 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Elegant Clean Navigation Menu Wrappers */
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }
    
    /* Style the radio menu options as premium individual interactive tiles */
    div[data-testid="stRadio"] > div {
        background-color: transparent !important;
        gap: 10px !important;
    }
    
    div[data-testid="stRadio"] label {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: none !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Hide the ugly standard radio circle completely */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]::before {
        display: none !important;
    }
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    div[data-testid="stRadio"] div[data-checked="true"] label {
        background-color: rgba(0, 242, 254, 0.06) !important;
        border-color: rgba(0, 242, 254, 0.4) !important;
        color: #00F2FE !important;
        border-left: 4px solid #00F2FE !important;
        box-shadow: 0 4px 12px rgba(0, 242, 254, 0.05) !important;
    }
    
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
    }

    /* BRAND HEADINGS STYLE */
    .sidebar-logo {
        font-size: 22px;
        font-weight: 800;
        color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: 1.5px;
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-logo span {
        color: #00F2FE;
    }
    
    .main-title {
        font-family: 'Impact', sans-serif !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        font-size: 38px !important;
        margin-bottom: 5px !important;
        letter-spacing: 1px;
    }
    
    /* NEON INPUT LABELS STYLE */
    label {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 1.5px;
        margin-bottom: 8px !important;
    }

    /* CYBERPUNK FORM COMPONENT DECORATION */
    .stTextInput input, .stTextArea textarea, div[data-testid="stSelectbox"] > div {
        background-color: #1E2235 !important;
        border: 1px solid #2D3450 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
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
    
    /* Neon focus highlight ring across both elements */
    .stTextInput input:focus, div[data-testid="stSelectbox"] > div:focus-within {
        border-color: #00F2FE !important;
        box-shadow: 0 0 8px rgba(0, 242, 254, 0.4) !important;
    }
    
    /* Fixed visibility of text hints inside inputs */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #64748B !important;
        opacity: 1 !important;
    }

    /* HIGH-VOLTAGE HYPER CYAN CTA ACTION BUTTON */
    div.stButton > button:first-child {
        background-color: #00F2FE !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
        padding: 0.6rem 2.2rem !important;
        box-shadow: 0 4px 14px rgba(0, 242, 254, 0.3);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #00B4D8 !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        transform: translateY(-1px);
    }
    
    /* Dark Balanced Clear Button */
    div.stButton > button[key*="clear_btn"] {
        background-color: #1E2235 !important;
        color: #94A3B8 !important;
        border: 1px solid #2D3450 !important;
        box-shadow: none !important;
    }
    div.stButton > button[key*="clear_btn"]:hover {
        background-color: #2D3450 !important;
        color: #FFFFFF !important;
    }
    
    /* CYBER INFRASTRUCTURE CONFIG BADGE */
    .status-badge {
        background-color: rgba(15, 23, 42, 0.6);
        color: #34D399;
        padding: 14px;
        border-radius: 8px;
        font-size: 12px;
        font-family: monospace;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Panel Navigation Matrix
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAIL<span>FLOW</span></div>', unsafe_allow_html=True)
    menu = st.radio("Nav", ["📝 Compose", "📅 Scheduled", "⏳ History"], label_visibility="collapsed")
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#34D399;">●</span> SYSTEM ONLINE<br><b style="color:white; font-family:sans-serif; font-size:11px;">Relay Connected</b></div>', unsafe_allow_html=True)

# --- PANEL BLOCK: COMPOSE LOOP ---
if "Compose" in menu:
    st.markdown('<div class="main-title">NEW EMAIL</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Compose and schedule your email distribution loop</div>', unsafe_allow_html=True)
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

    # 2. High-Contrast Status Display Blocks
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
                    <div style="background-color: #1E293B; border-left: 5px solid #38BDF8; padding: 15px; border-radius: 6px; margin-top: 20px;">
                        <b style="color: #38BDF8; font-size: 15px;">📅 Scheduled Successfully</b><br>
                        <span style="color: #94A3B8; font-size: 13px;">Outbound email successfully saved to your scheduled queue!</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                status_box = st.empty()
                status_box.markdown("""
                    <div style="background-color: #2D2514; border-left: 5px solid #F59E0B; padding: 15px; border-radius: 6px; margin-top: 20px;">
                        <b style="color: #F59E0B; font-size: 15px;">⏳ Sending email...</b><br>
                        <span style="color: #A1A1AA; font-size: 13px;">Accessing Google API cloud relays. Please wait...</span>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    # Deliver via our authenticated Gmail API script connection
                    send_email(to_field, subject_field, body_field)
                    st.session_state.email_history.append(email_payload)
                    
                    status_box.markdown("""
                        <div style="background-color: #064E3B; border-left: 5px solid #10B981; padding: 15px; border-radius: 6px; margin-top: 20px;">
                            <b style="color: #34D399; font-size: 15px;">✅ Email sent successfully!</b><br>
                            <span style="color: #A7F3D0; font-size: 13px;">Dispatch confirmed. Message has left your Gmail account safely.</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.toast("Email Dispatched!", icon="🚀")
                    
                except Exception as e:
                    status_box.markdown(f"""
                        <div style="background-color: #4C1D1D; border-left: 5px solid #EF4444; padding: 15px; border-radius: 6px; margin-top: 20px;">
                            <b style="color: #F87171; font-size: 15px;">❌ Delivery Failed</b><br>
                            <span style="color: #FCA5A5; font-size: 13px;">Handshake Refused: {str(e)}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #4C1D1D; border-left: 5px solid #EF4444; padding: 15px; border-radius: 6px; margin-top: 20px;">
                    <b style="color: #F87171; font-size: 15px;">⚠️ Validation Error</b><br>
                    <span style="color: #FCA5A5; font-size: 13px;">Please make sure the TO, SUBJECT, and MESSAGE blocks are filled out.</span>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL BLOCK: SCHEDULED ---
elif "Scheduled" in menu:
    st.markdown('<div class="main-title">SCHEDULED EMAILS</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Emails currently queued up for future automated delivery</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.scheduled_emails:
        st.markdown('<div style="text-align: center; padding: 5rem 2rem; color: #64748B; font-family: monospace; font-size: 16px;">📅 No scheduled emails in your dispatch queue.</div>', unsafe_allow_html=True)
    else:
        st.write(st.session_state.scheduled_emails)

# --- PANEL BLOCK: HISTORY ---
elif "History" in menu:
    st.markdown('<div class="main-title">TRANSMISSION HISTORY</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94A3B8; font-size: 14px; margin-bottom: 20px;">Log of all successfully dispatched automated emails</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.email_history:
        st.markdown('<div style="text-align: center; padding: 5rem 2rem; color: #64748B; font-family: monospace; font-size: 16px;">⏳ No tracked sent logs available yet.</div>', unsafe_allow_html=True)
    else:
        st.write(st.session_state.email_history)
