import streamlit as st
from datetime import datetime
# Import your secured engine logic
from email_service import send_email

# 1. Initialize Persistent Application State Trackers
if "scheduled_emails" not in st.session_state:
    st.session_state.scheduled_emails = []
if "email_history" not in st.session_state:
    st.session_state.email_history = []

st.set_page_config(page_title="MailFlow", page_icon="✉️", layout="wide")

# 2. Executive Theme & Custom Layout Engine Injection
st.markdown("""
    <style>
    /* PREVENT SCREEN OVERFLOW & MATCH DESIGN CANVAS */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding: 2rem min(4vw, 3rem) !important;
        max-width: 1400px;
    }
    
    /* --- SIDEBAR NAVIGATION BRAND STYLING --- */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    .sidebar-logo {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.5px;
        padding: 0.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-logo span {
        color: #E05621;
    }
    
    /* MAIN TITLE HEADING FIX FOR CLIPPING */
    .main-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        font-size: 32px !important;
        line-height: 1.3 !important;
        margin-top: 5px !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.5px;
        display: block !important;
    }
    
    /* FIELD LABELS */
    label, .custom-input-label {
        color: #475569 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 0.5px;
        margin-bottom: 6px !important;
        display: block;
    }

    /* PRISTINE CRISP WHITE FORM FIELD CONTROLS */
    .stTextInput input, .stTextArea textarea, 
    div[data-testid="stSelectbox"] > div,
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        color: #0F172A !important;
        font-size: 14px !important;
        transition: all 0.15s ease-in-out;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }

    .stTextInput input {
        height: 42px !important;
        padding: 8px 12px !important;
    }
    .stTextArea textarea {
        padding: 10px 12px !important;
    }

    /* Target the text input element container by looking for our explicit label name match */
    div[data-testid="element-container"]:has(label:contains("SCHEDULE DATE & TIME")) input,
    div[data-testid="element-container"]:has(input[aria-label="SCHEDULE DATE & TIME"]) input {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23E05621' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='18' rx='2' ry='2'%3E%3C/rect%3E%3Cline x1='16' y1='2' x2='16' y2='6'%3E%3C/line%3E%3Cline x1='8' y1='2' x2='8' y2='6'%3E%3C/line%3E%3Cline x1='3' y1='10' x2='21' y2='10'%3E%3C/line%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: calc(100% - 14px) center !important;
        padding-right: 40px !important;
    }

    /* Selectbox Custom Adjustments */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        height: 42px !important;
        background-color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
        background-color: transparent !important;
        padding-top: 5px !important;
        padding-left: 4px !important;
        color: #0F172A !important;
    }
    
    /* MATCHING ORANGE DESIGN SYSTEM THEME ICON ACCENTS */
    div[data-testid="stSelectbox"] svg {
        color: #E05621 !important;
    }
    
    /* Active Focus Styles */
    .stTextInput input:focus, .stTextArea textarea:focus, 
    div[data-testid="stSelectbox"] > div:focus-within {
        border-color: #1A56DB !important;
        box-shadow: 0 0 0 3px rgba(26, 86, 219, 0.15) !important;
        outline: none !important;
    }

    /* --- SIDEBAR RADIO BUTTON NAVIGATION OVERRIDES --- */
    div[data-testid="stRadio"] > div {
        background-color: transparent !important;
        gap: 6px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        color: #94A3B8 !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        width: 100% !important;
    }
    
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]::before,
    div[data-testid="stRadio"] div[data-testid="stWidgetWrapped-true"] {
        display: none !important;
    }
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    
    /* Active Orange Navigation Tab Background Style */
    div[data-testid="stRadio"] div[data-checked="true"] label {
        background-color: #E05621 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(224, 86, 33, 0.25) !important;
    }
    
    div[data-testid="stRadio"] label:hover:not([data-checked="true"]) {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
    }

    /* BUTTON ACTION BAR CONTROLS */
    div.stButton > button:first-child {
        background-color: #E05621 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: 1px solid #E05621 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0.6rem 1.75rem !important;
        transition: all 0.15s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #C2410C !important;
        border-color: #C2410C !important;
    }
    
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #D1D5DB !important;
    }
    div.stButton > button[key*="clear_btn"]:hover {
        background-color: #F9FAFB !important;
    }
    
    /* SYSTEM STATUS FOOTER PANEL */
    .status-badge {
        background-color: #0F172A;
        color: #34D399;
        padding: 12px;
        border-radius: 6px;
        font-size: 12px;
        border: 1px solid #334155;
    }
    
    hr {
        margin: 1.25rem 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation Structure
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAIL<span>FLOW</span></div>', unsafe_allow_html=True)
    
    scheduled_count = len(st.session_state.scheduled_emails)
    history_count = len(st.session_state.email_history)
    
    menu = st.radio(
        "Navigation Menu", 
        [
            "📝  Compose", 
            f"📅  Scheduled      {scheduled_count}", 
            f"⏳  History          {history_count}"
        ], 
        label_visibility="collapsed"
    )
    
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.markdown('<div class="status-badge"><span style="color:#10B981;">●</span> Gmail ready<br><span style="color:#94A3B8; font-size:11px;">Configured & Active</span></div>', unsafe_allow_html=True)

# --- PANEL BLOCK: COMPOSE LOOP ---
if "Compose" in menu:
    st.markdown('<div class="main-title">New Email</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #64748B; font-size: 14px; margin-bottom: 10px;">Compose and schedule your email distribution loops</div>', unsafe_allow_html=True)
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        to_field = st.text_input("TO", placeholder="recipient@example.com", key="compose_to_field")
    with col2:
        from_field = st.text_input("FROM (YOUR GMAIL)", placeholder="you@gmail.com", key="compose_from_field")
        
    subject_field = st.text_input("SUBJECT", placeholder="Email subject line", key="compose_subject_field")
    body_field = st.text_area("MESSAGE", placeholder="Write your message here...", height=150, key="compose_body_field")

    col3, col4 = st.columns(2)
    with col3:
        # Crisp input text node
        datetime_value = st.text_input("SCHEDULE DATE & TIME", value="2026-05-31 12:01 PM", key="compose_date_field")
        
    with col4:
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"], key="compose_send_mode")
        
    st.write("")

    # Interaction Action Row Bar
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([6, 1, 1.2])
    with ctrl_col2:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.rerun()
            
    with ctrl_col3:
        send_clicked = st.button("Send Email", key="send_btn", use_container_width=True)

    # Feedback Engine Processing Cards
    if send_clicked:
        if to_field and subject_field and body_field:
            email_payload = {
                "to": to_field,
                "from": from_field,
                "subject": subject_field,
                "body": body_field,
                "timestamp": datetime_value
            }
            
            if "Schedule for later" in send_mode:
                st.session_state.scheduled_emails.append(email_payload)
                st.toast("Email Queued Successfully!", icon="📅")
                st.rerun()
            else:
                status_box = st.empty()
                status_box.markdown("""
                    <div style="background-color: #FFFBEB; border-left: 4px solid #D97706; padding: 10px; border-radius: 6px; margin-top: 10px;">
                        <b style="color: #92400E; font-size: 14px;">⏳ Dispatched Processing...</b>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    send_email(to_field, subject_field, body_field)
                    st.session_state.email_history.append(email_payload)
                    st.toast("Email Sent Successfully!", icon="🚀")
                    st.rerun()
                    
                except Exception as e:
                    status_box.markdown(f"""
                        <div style="background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 10px; border-radius: 6px; margin-top: 10px;">
                            <b style="color: #991B1B; font-size: 14px;">❌ Connection Error:</b> <span style="color: #4B5563; font-size: 13px;">{str(e)}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 10px; border-radius: 6px; margin-top: 10px;">
                    <b style="color: #991B1B; font-size: 14px;">⚠️ Missing Parameters:</b> <span style="color: #4B5563; font-size: 13px;">Please complete To, Subject, and Message fields.</span>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL BLOCK: SCHEDULED ---
elif "Scheduled" in menu:
    st.markdown('<div class="main-title">Scheduled Emails</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.scheduled_emails:
        st.info("No scheduled emails in your dispatch queue.")
    else:
        st.write(st.session_state.scheduled_emails)

# --- PANEL BLOCK: HISTORY ---
elif "History" in menu:
    st.markdown('<div class="main-title">Transmission History</div>', unsafe_allow_html=True)
    st.write("---")
    if not st.session_state.email_history:
        st.info("No sent logs tracked yet.")
    else:
        st.write(st.session_state.email_history)
