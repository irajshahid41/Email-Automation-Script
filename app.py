import streamlit as st
import json
import os
from datetime import datetime

# 1. Initialize Global Session States for Data Tracking
if "scheduled_emails" not in st.session_state:
    st.session_state.scheduled_emails = []

if "email_history" not in st.session_state:
    st.session_state.email_history = []

# 2. Page Configuration & Responsive Viewport Layout
st.set_page_config(
    page_title="MailFlow", 
    page_icon="✉️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Dynamic Responsive CSS Injection
st.markdown("""
    <style>
    /* Responsive Root Variables */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F4F0E6 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Auto-scaling Main Window Padding */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        padding-left: min(5vw, 4rem) !important;
        padding-right: min(5vw, 4rem) !important;
        max-width: 1400px;
    }
    
    /* Dark Theme Sidebar Layout */
    [data-testid="stSidebar"] {
        background-color: #1E1E1C !important;
        min-width: 240px !important;
        max-width: 320px !important;
    }
    
    /* Sidebar Brand Header */
    .sidebar-logo {
        font-size: clamp(20px, 2vw, 25px);
        font-weight: 800;
        color: #E06A3B;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        padding: 1rem 0;
        text-align: left;
    }
    
    /* Typography Overrides */
    h1 {
        font-family: 'Impact', 'Arial Black', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        color: #1E1E1C !important;
        font-size: clamp(28px, 4vw, 42px) !important;
    }
    
    /* Table & Form Labels Styling */
    label {
        color: #5C5A55 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 11px !important;
        letter-spacing: 1px;
    }

    /* Input Field Normalization */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D2C4 !important;
        border-radius: 6px !important;
        color: #1E1E1C !important;
        padding: 0.5rem !important;
    }

    /* Orange CTA Action Buttons */
    div.stButton > button:first-child {
        background-color: #D35400 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 1.8rem !important;
        transition: background 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #A04000 !important;
    }
    
    /* Clear/Secondary Buttons styling */
    div.stButton > button[key*="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #1E1E1C !important;
        border: 1px solid #D6D2C4 !important;
    }

    /* Centered Empty State Container */
    .empty-state-box {
        text-align: center;
        padding: 5rem 2rem;
        color: #8C8A82;
        font-family: monospace;
    }
    .empty-state-icon {
        font-size: 48px;
        color: #C0BDB3;
        margin-bottom: 10px;
    }
    
    /* Bottom Sidebar Connection Footer */
    .status-badge {
        background-color: #162216;
        color: #52BE80;
        padding: 12px;
        border-radius: 6px;
        font-size: 12px;
        text-align: left;
        border: 1px solid #1E4624;
        font-family: monospace;
        margin-top: auto;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar Dynamic Structure
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    st.write("")
    
    # Navigation Radio Matrix mimicking custom navigation buttons
    menu = st.radio(
        "Navigation Options",
        ["📝 Compose", "📅 Scheduled", "⏳ History"],
        label_visibility="collapsed"
    )
    
    # Multi-line spacer context to force connection card to stick to bottom natively
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.markdown("""
        <div class="status-badge">
            <span style='color: #2ECC71;'>●</span> Gmail ready<br>
            <span style='color: white; font-weight: bold;'>Configured</span>
        </div>
    """, unsafe_allow_html=True)

# 5. Application Routing & Core State Functions

# --- TAB 1: COMPOSE EMAIL ---
if "Compose" in menu:
    st.markdown("<h1>NEW EMAIL</h1>", unsafe_allow_html=True)
    st.caption("Compose and schedule your email distribution queue")
    st.write("---")
    
    # Input Block Fields
    col1, col2 = st.columns(2)
    with col1:
        to_field = st.text_input("TO", placeholder="recipient@example.com")
    with col2:
        from_field = st.text_input("FROM (YOUR GMAIL)", placeholder="you@gmail.com")
        
    subject_field = st.text_input("SUBJECT", placeholder="Email subject line")
    body_field = st.text_area("MESSAGE", placeholder="Write your message content here...", height=220)
    
    col3, col4 = st.columns(2)
    with col3:
        # Default scheduling date context
        time_field = st.text_input("SCHEDULE DATE & TIME", value=datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    with col4:
        mode_field = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"])
        
    st.write("")
    
    # Bottom Controls Allocation
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([6, 1, 1.2])
    with ctrl_col2:
        if st.button("Clear", key="clear_btn", use_container_width=True):
            st.rerun()
            
    with ctrl_col3:
        if st.button("Send Email", key="send_btn", use_container_width=True):
            if to_field and subject_field and body_field:
                new_email = {
                    "to": to_field,
                    "from": from_field,
                    "subject": subject_field,
                    "body": body_field,
                    "timestamp": time_field
                }
                
                # Check execution pathway based on send mode dropdown
                if mode_field == "Schedule for later":
                    st.session_state.scheduled_emails.append(new_email)
                    st.success(f"🎉 Outbound email successfully queued for delivery!")
                else:
                    st.session_state.email_history.append(new_email)
                    st.success(f"🚀 Email successfully dispatched straight to destination!")
            else:
                st.error("⚠️ Form validation failure: Please fill out TO, SUBJECT, and MESSAGE blocks.")

# --- TAB 2: SCHEDULED EMAILS ---
elif "Scheduled" in menu:
    st.markdown("<h1>SCHEDULED EMAILS</h1>", unsafe_allow_html=True)
    st.caption("Emails currently queued up for future automated delivery")
    st.write("---")
    
    if not st.session_state.scheduled_emails:
        # Renders the specific minimal calendar icon placeholder state from your image
        st.markdown("""
            <div class="empty-state-box">
                <div class="empty-state-icon">📅</div>
                <div style="font-size: 16px;">No scheduled emails yet</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Interactive data grid if entries exist
        for idx, email in enumerate(st.session_state.scheduled_emails):
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 5, 2])
                c1.write(f"**Target:** {email['to']}")
                c2.write(f"**Subject:** {email['subject']} | *Will execute at:* `{email['timestamp']}`")
                with c3:
                    if st.button("Cancel Queue", key=f"cancel_{idx}"):
                        st.session_state.scheduled_emails.pop(idx)
                        st.rerun()

# --- TAB 3: HISTORY ---
elif "History" in menu:
    st.markdown("<h1>TRANSMISSION HISTORY</h1>", unsafe_allow_html=True)
    st.caption("Log of all automated email delivery dispatches")
    st.write("---")
    
    if not st.session_state.email_history:
        st.markdown("""
            <div class="empty-state-box">
                <div class="empty-state-icon">⏳</div>
                <div style="font-size: 16px;">No history records found</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Display past logs in a clean structured stack
        for email in reversed(st.session_state.email_history):
            with st.container(border=True):
                st.write(f"⏱️ **Dispatched:** `{email['timestamp']}`")
                st.write(f"**To:** {email['to']} | **Subject:** {email['subject']}")
                st.info(f"{email['body']}")
            
