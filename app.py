import streamlit as st
from datetime import datetime
from email_service import send_email

# 1. Initialize Persistent Application State Trackers
if "scheduled_emails" not in st.session_state:
    st.session_state.scheduled_emails = []
if "email_history" not in st.session_state:
    st.session_state.email_history = []

st.set_page_config(page_title="MailFlow", page_icon="✉️", layout="wide")

# 2. Executive Theme & Custom Layout Engine
st.markdown("""
    <style>
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; }
    .block-container { padding: 2rem min(4vw, 3rem) !important; max-width: 1400px; }
    [data-testid="stSidebar"] { background-color: #1E293B !important; }
    
    /* Sidebar Logo */
    .sidebar-logo { font-size: 22px; font-weight: 700; color: #FFFFFF; padding: 0.5rem 0 1.5rem 0; display: flex; align-items: center; gap: 10px; }
    .sidebar-logo span { color: #E05621; }
    
    /* Title & Labels */
    .main-title { font-weight: 700 !important; color: #0F172A !important; font-size: 32px !important; margin-bottom: 2px !important; }
    .custom-input-label { color: #475569 !important; font-weight: 600 !important; text-transform: uppercase; font-size: 11px !important; margin-bottom: 6px !important; display: block; }
    
    /* Date Input Fix: Container + Icon */
    .date-input-wrapper { position: relative; }
    div[data-testid="stTextInput"] input { padding-right: 45px !important; }
    .calendar-icon {
        position: absolute;
        right: 15px;
        top: 36px;
        pointer-events: none;
        font-size: 16px;
        z-index: 10;
    }
    
    /* Buttons */
    div.stButton > button:first-child { background-color: #E05621 !important; color: #FFFFFF !important; border-radius: 6px !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAIL<span>FLOW</span></div>', unsafe_allow_html=True)
    menu = st.radio("Navigation", ["📝 Compose", "📅 Scheduled", "⏳ History"], label_visibility="collapsed")
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.markdown('<div class="status-badge" style="background-color: #0F172A; color: #34D399; padding: 12px; border-radius: 6px; font-size: 12px;">● Gmail ready</div>', unsafe_allow_html=True)

# 4. Main Compose Panel
if "Compose" in menu:
    st.markdown('<div class="main-title">New Email</div>', unsafe_allow_html=True)
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
        st.markdown('<label class="custom-input-label">SCHEDULE DATE & TIME</label>', unsafe_allow_html=True)
        # We wrap in a div to allow absolute positioning of the icon
        st.markdown('<div class="date-input-wrapper">', unsafe_allow_html=True)
        datetime_value = st.text_input("SCHEDULE DATE & TIME", value="2026-05-31 12:01 PM", key="compose_date_field", label_visibility="collapsed")
        st.markdown('<span class="calendar-icon">📅</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col4:
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"], key="compose_send_mode")
        
    if st.button("Send Email", use_container_width=True):
        if to_field and subject_field:
            email_payload = {"to": to_field, "subject": subject_field, "body": body_field, "timestamp": datetime_value}
            if "Schedule" in send_mode:
                st.session_state.scheduled_emails.append(email_payload)
                st.toast("Email Queued!", icon="📅")
            else:
                send_email(to_field, subject_field, body_field)
                st.session_state.email_history.append(email_payload)
                st.toast("Email Sent!", icon="🚀")
            st.rerun()
        else:
            st.error("Please fill in the required fields.")

elif "Scheduled" in menu:
    st.markdown('<div class="main-title">Scheduled Emails</div>', unsafe_allow_html=True)
    st.write(st.session_state.scheduled_emails)

elif "History" in menu:
    st.markdown('<div class="main-title">Transmission History</div>', unsafe_allow_html=True)
    st.write(st.session_state.email_history)
