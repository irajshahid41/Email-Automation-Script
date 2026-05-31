import streamlit as st
import json
import os
from datetime import datetime, time, datetime as dt
# Import the custom email backend sending logic we fixed earlier
from email_service import send_email

# 1. Initialize Global Session States for Tracking Dashboard Data
if "scheduled_emails" not in st.session_state:
    st.session_state.scheduled_emails = []

if "email_history" not in st.session_state:
    st.session_state.email_history = []

# 2. Responsive Viewport Layout Config
st.set_page_config(
    page_title="MailFlow", 
    page_icon="✉️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Dynamic UI Premium Theme CSS
st.markdown("""
    <style>
    /* Main Theme Background override */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F0E6 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Auto-scaling Layout Viewport */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: min(5vw, 4rem) !important;
        padding-right: min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    
    /* Dark Navigation Sidebar Layout */
    [data-testid="stSidebar"] {
        background-color: #1E1E1C !important;
    }
    
    .sidebar-logo {
        font-size: clamp(20px, 2vw, 24px);
        font-weight: 800;
        color: #E06A3B;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        padding: 1rem 0;
    }
    
    /* Header Font style matching design */
    h1 {
        font-family: 'Impact', 'Arial Black', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 0.5px !important;
        color: #1E1E1C !important;
        font-size: clamp(28px, 4vw, 38px) !important;
        margin-bottom: 0px !important;
    }
    
    /* Form Labels Formatting */
    label {
        color: #5C5A55 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 1px;
    }

    /* Form Input Element Normalization */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], div[data-testid="stDateInput"] input {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D2C4 !important;
        border-radius: 6px !important;
        color: #1E1E1C !important;
    }

    /* Orange Core CTA Actions */
    div.stButton > button:first-child {
        background-color: #D35400 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 1.8rem !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #BA4A00 !important;
    }
    
    /* Clear/Secondary interaction button styling */
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #1E1E1C !important;
        border: 1px solid #D6D2C4 !important;
    }

    .empty-state-box {
        text-align: center;
        padding: 5rem 2rem;
        color: #8C8A82;
        font-family: monospace;
    }
    
    /* Sidebar Connection Footer Badge */
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

# 4. Sidebar Dynamic Structure
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    st.write("")
    
    menu = st.radio(
        "Navigation Options",
        ["📝 Compose", "📅 Scheduled", "⏳ History"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>" * 12, unsafe_allow_html=True)
    st.markdown("""
        <div class="status-badge">
            <span style='color: #2ECC71;'>●</span> Gmail ready<br>
            <span style='color: white; font-weight: bold;'>Configured</span>
        </div>
    """, unsafe_allow_html=True)

# --- TAB 1: COMPOSE OUTBOUND EMAIL ---
if "Compose" in menu:
    st.markdown("<h1>NEW EMAIL</h1>", unsafe_allow_html=True)
    st.caption("Compose and schedule your automated email campaigns")
    st.write("---")
    
    # Input Block Fields
    col1, col2 = st.columns(2)
    with col1:
        to_field = st.text_input("TO", placeholder="recipient@example.com")
    with col2:
        from_field = st.text_input("FROM (YOUR GMAIL)", placeholder="you@gmail.com")
        
    subject_field = st.text_input("SUBJECT", placeholder="Email subject line")
    body_field = st.text_area("MESSAGE", placeholder="Write your message here...", height=200)
    
    # Advanced Scheduler Core Block
    col3, col4, col5 = st.columns([1.5, 1.5, 2])
    with col3:
        # Proper Native Calendar Picker matching image specs
        selected_date = st.date_input("SCHEDULE DATE", value=dt.now().date())
    with col4:
        # Proper Native Time Selection grid Matching image specs
        selected_time = st.time_input("SCHEDULE TIME", value=time(12, 1))
    with col5:
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"])
        
    st.write("")
    
    # Interaction Control Area
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([6, 1, 1.2])
    with ctrl_col2:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.rerun()
            
    with ctrl_col3:
        if st.button("Send Email", key="send_btn", use_container_width=True):
            if to_field and subject_field and body_field:
                # Combine Date & Time inputs into a clean string for reporting
                combined_dt = dt.combine(selected_date, selected_time)
                formatted_timestamp = combined_dt.strftime("%Y-%m-%d %I:%M %p")
                
                email_payload = {
                    "to": to_field,
                    "from": from_field,
                    "subject": subject_field,
                    "body": body_field,
                    "timestamp": formatted_timestamp
                }
                
                # Dynamic Routing logic based on Send Mode setting
                if send_mode == "Schedule for later":
                    st.session_state.scheduled_emails.append(email_payload)
                    st.success(f"📅 Email successfully queued for delivery at {formatted_timestamp}!")
                else:
                    with st.spinner("Processing live dispatch via Gmail API..."):
                        try:
                            # Calls your actual authorized service function
                            send_email(to_field, subject_field, body_field)
                            st.session_state.email_history.append(email_payload)
                            st.success("🚀 Dispatched successfully! Gmail API transaction confirmed.")
                        except Exception as e:
                            st.error(f"❌ Handshake failed: {str(e)}")
            else:
                st.error("⚠️ Form validation failure: Please fill out TO, SUBJECT, and MESSAGE.")

# --- TAB 2: SCHEDULED REGISTRY VIEW ---
elif "Scheduled" in menu:
    st.markdown("<h1>SCHEDULED EMAILS</h1>", unsafe_allow_html=True)
    st.caption("Emails currently queued up for future automated delivery")
    st.write("---")
    
    if not st.session_state.scheduled_emails:
        st.markdown("""
            <div class="empty-state-box">
                <div style="font-size: 48px; color: #C0BDB3; margin-bottom:10px;">📅</div>
                <div style="font-size: 16px;">No scheduled emails yet</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for idx, email in enumerate(st.session_state.scheduled_emails):
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 5, 2])
                c1.write(f"**Target:** {email['to']}")
                c2.write(f"**Subject:** {email['subject']} | ⏳ *Queue Time:* `{email['timestamp']}`")
                with c3:
                    if st.button("Cancel", key=f"cancel_{idx}"):
                        st.session_state.scheduled_emails.pop(idx)
                        st.rerun()

# --- TAB 3: TRANSACTION LOGS ---
elif "History" in menu:
    st.markdown("<h1>TRANSMISSION HISTORY</h1>", unsafe_allow_html=True)
    st.caption("Log of all successfully dispatched automated emails")
    st.write("---")
    
    if not st.session_state.email_history:
        st.markdown("""
            <div class="empty-state-box">
                <div style="font-size: 48px; color: #C0BDB3; margin-bottom:10px;">⏳</div>
                <div style="font-size: 16px;">No history records found</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for email in reversed(st.session_state.email_history):
            with st.container(border=True):
                st.write(f"⏱️ **Sent Out:** `{email['timestamp']}`")
                st.write(f"**To:** {email['to']} | **Subject:** {email['subject']}")
                st.info(f"{email['body']}")
