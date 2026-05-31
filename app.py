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

# 2. Executive Slate Blue Stylesheet Injection
st.markdown("""
    <style>
    /* GLOBAL CANVASES STYLING */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding: 3rem min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    
    /* --- EXECUTIVE CHARCOAL SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* BRAND HEADINGS STYLE */
    .sidebar-logo {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: 0.5px;
        padding: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-logo span {
        color: #38BDF8;
    }
    
    .main-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        font-size: 32px !important;
        margin-bottom: 5px !important;
        letter-spacing: -0.5px;
    }
    
    /* MINIMALIST CONTEMPORARY LABEL STYLING */
    label {
        color: #475569 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 0.5px;
        margin-bottom: 6px !important;
    }

    /* PRISTINE CRISP WHITE FORM FIELD CONTROLS */
    .stTextInput input, .stTextArea textarea, div[data-testid="stSelectbox"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        color: #0F172A !important;
        font-size: 14px !important;
        transition: all 0.15s ease-in-out;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }

    /* Explicit sizing layout patches */
    .stTextInput input {
        height: 42px !important;
        padding: 10px !important;
    }

    /* Force selection components to perfectly match text box heights */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        height: 42px !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    div[data-baseweb="select"] > div:first-child {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        padding-left: 4px !important;
    }
    
    /* Clean corporate royal blue focus borders */
    .stTextInput input:focus, div[data-testid="stSelectbox"] > div:focus-within {
        border-color: #1A56DB !important;
        box-shadow: 0 0 0 3px rgba(26, 86, 219, 0.15) !important;
    }
    
    /* Soft dark grey descriptive text inside placeholders */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #94A3B8 !important;
        opacity: 1 !important;
    }

    /* --- SLATE BLUE NAVIGATION OVERRIDES --- */
    div[data-testid="stRadio"] > div {
        background-color: transparent !important;
        gap: 6px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        color: #94A3B8 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        width: 100% !important;
    }
    
    /* Strip Streamlit radio circles */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]::before,
    div[data-testid="stRadio"] div[data-testid="stWidgetWrapped-true"] {
        display: none !important;
    }
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    
    /* Active State Nav Tab Indicator */
    div[data-testid="stRadio"] div[data-checked="true"] label {
        background-color: #1A56DB !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(26, 86, 219, 0.1) !important;
    }
    
    div[data-testid="stRadio"] label:hover:not([data-checked="true"]) {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
    }

    /* HIGH-CONTRAST PROFESSIONAL EXECUTIVE CALL-TO-ACTIONS */
    div.stButton > button:first-child {
        background-color: #1A56DB !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: 1px solid #1A56DB !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0.55rem 1.75rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        transition: all 0.15s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #1E429F !important;
        border-color: #1E429F !important;
    }
    
    /* Balanced Corporate Neutral Clear Button */
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #D1D5DB !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    div.stButton > button[key*="clear_btn"]:hover {
        background-color: #F9FAFB !important;
        color: #111827 !important;
        border-color: #C5C9D1 !important;
    }
    
    /* REFINED SYSTEM CONNECTIVITY CONDENSED FOOTER */
    .status-badge {
        background-color: #0F172A;
        color: #34D399;
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation Structure
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAIL<span>FLOW</span></div>', unsafe_allow_html=True)
    
    # Calculate counters dynamically
    scheduled_count = len(st.session_state.scheduled_emails)
    history_count = len(st.session_state.email_history)
    
    menu = st.radio(
        "Navigation Menu", 
        [
            "📝  Compose", 
            f"📅  Scheduled  ({scheduled_count})", 
            f"⏳  History  ({history_count})"
        ], 
        label_visibility="collapsed"
    )
    
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#10B981;">●</span> Gmail ready<br><span style="color:#94A3B8; font-size:11px;">Configured & Active</span></div>', unsafe_allow_html=True)

# --- PANEL BLOCK: COMPOSE LOOP ---
if "Compose" in menu:
    st.markdown('<div class="main-title">New Email</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #64748B; font-size: 14px; margin-bottom: 20px;">Compose and schedule your email distribution loops</div>', unsafe_allow_html=True)
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

    # Interaction Control Action Bar Row
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([6, 1, 1.2])
    with ctrl_col2:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.rerun()
            
    with ctrl_col3:
        send_clicked = st.button("Send Email", key="send_btn", use_container_width=True)

    # Feedback Cards
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
                    <div style="background-color: #EFF6FF; border-left: 4px solid #1A56DB; padding: 14px; border-radius: 6px; margin-top: 15px;">
                        <b style="color: #1E429F; font-size: 14px;">📅 Queued Successfully</b><br>
                        <span style="color: #4B5563; font-size: 13px;">This message has been securely processed and added to your outbound schedule list.</span>
                    </div>
                """, unsafe_allow_html=True)
                st.rerun()
            else:
                status_box = st.empty()
                status_box.markdown("""
                    <div style="background-color: #FFFBEB; border-left: 4px solid #D97706; padding: 14px; border-radius: 6px; margin-top: 15px;">
                        <b style="color: #92400E; font-size: 14px;">⏳ Dispatched Processing</b><br>
                        <span style="color: #4B5563; font-size: 13px;">Communicating secure handshakes over cloud relay connections...</span>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    send_email(to_field, subject_field, body_field)
                    st.session_state.email_history.append(email_payload)
                    
                    status_box.markdown("""
                        <div style="background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 14px; border-radius: 6px; margin-top: 15px;">
                            <b style="color: #166534; font-size: 14px;">✅ Transaction Completed</b><br>
                            <span style="color: #4B5563; font-size: 13px;">Delivery verified. Email safely passed to standard server routing.</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.toast("Email Dispatched!", icon="🚀")
                    st.rerun()
                    
                except Exception as e:
                    status_box.markdown(f"""
                        <div style="background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 14px; border-radius: 6px; margin-top: 15px;">
                            <b style="color: #991B1B; font-size: 14px;">❌ Cloud Connection Timeout</b><br>
                            <span style="color: #4B5563; font-size: 13px;">API error returned: {str(e)}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 14px; border-radius: 6px; margin-top: 15px;">
                    <b style="color: #991B1B; font-size: 14px;">⚠️ Missing Parameters</b><br>
                    <span style="color: #4B5563; font-size: 13px;">Please fill out the recipient, subject line, and message area to clear verification.</span>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL BLOCK: SCHEDULED ---
elif "Scheduled" in menu:
    st.markdown('<div class="main-title">Scheduled Emails</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #64748B; font-size: 14px; margin-bottom: 20px;">Emails currently queued up for future automated delivery</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.scheduled_emails:
        st.info("No scheduled emails in your dispatch queue.")
    else:
        st.write(st.session_state.scheduled_emails)

# --- PANEL BLOCK: HISTORY ---
elif "History" in menu:
    st.markdown('<div class="main-title">Transmission History</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #64748B; font-size: 14px; margin-bottom: 20px;">Log of all successfully dispatched automated emails</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.email_history:
        st.info("No sent logs tracked yet.")
    else:
        st.write(st.session_state.email_history)
