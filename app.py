import streamlit as st
from datetime import datetime

# 1. Set Page Configuration
st.set_page_config(page_title="MailFlow", page_icon="✉️", layout="wide")

# 2. Inject Custom CSS for the Retro/Modern SaaS Theme
st.markdown("""
    <style>
    /* Main Background Color */
    .stApp {
        background-color: #F4F0E6; 
    }
    
    /* Sidebar styling Override */
    [data-testid="stSidebar"] {
        background-color: #1E1E1C !important;
    }
    
    /* Sidebar Text / Title */
    .sidebar-logo {
        font-size: 24px;
        font-weight: bold;
        color: #E06A3B;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        padding-bottom: 20px;
    }
    
    /* Input Labels Styling */
    label {
        color: #5C5A55 !important;
        font-weight: bold !important;
        text-transform: uppercase;
        font-size: 12px !important;
        letter-spacing: 1px;
    }

    /* Input Boxes Custom Look */
    .stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D2C4 !important;
        border-radius: 6px !important;
        color: #1E1E1C !important;
    }

    /* Main Action Button (Send Email) */
    div.stButton > button:first-child {
        background-color: #D35400 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 2rem !important;
    }
    
    /* Clear Button Customization */
    div.stButton > button[key="clear_btn"] {
        background-color: #FFFFFF !important;
        color: #1E1E1C !important;
        border: 1px solid #D6D2C4 !important;
    }
    
    /* Status Badge styling */
    .status-badge {
        background-color: #243324;
        color: #76D7C4;
        padding: 8px;
        border-radius: 6px;
        font-size: 13px;
        text-align: center;
        border: 1px solid #27AE60;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation Area
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✉️ MAILFLOW</div>', unsafe_allow_html=True)
    st.write("")
    
    # Navigation menu simulating the design tabs
    menu = st.radio(
        "Navigation",
        ["📝 Compose", "📅 Scheduled", "⏳ History"],
        label_visibility="collapsed"
    )
    
    # Pushes the status indicator box to the very bottom of the sidebar
    st.vget_spacer() if hasattr(st, "vget_spacer") else st.write("\n" * 15)
    st.markdown('<div class="status-badge">🟢 Gmail Ready<br><b style="color:white;">Configured</b></div>', unsafe_allow_html=True)

# 4. Main Window Content
if "Compose" in menu:
    st.title("NEW EMAIL")
    st.caption("Compose and schedule your email")
    st.write("---")
    
    # Row 1: To and From Fields
    col1, col2 = st.columns(2)
    with col1:
        to_email = st.text_input("TO", placeholder="recipient@example.com")
    with col2:
        from_email = st.text_input("FROM (YOUR GMAIL)", placeholder="you@gmail.com")
        
    # Row 2: Subject Field
    subject = st.text_input("SUBJECT", placeholder="Email subject line")
    
    # Row 3: Message Body Area
    body = st.text_area("MESSAGE", placeholder="Write your message here...", height=200)
    
    # Row 4: Scheduling Controls
    col3, col4 = st.columns(2)
    with col3:
        schedule_time = st.text_input("SCHEDULE DATE & TIME", value="2026-05-31 12:01 PM")
    with col4:
        send_mode = st.selectbox("SEND MODE", ["Send Immediately", "Schedule for later"])
        
    st.write("")
    
    # Row 5: Interaction Buttons aligned right
    btn_col1, btn_col2, btn_col3 = st.columns([6, 1, 1.2])
    with btn_col2:
        st.button("Clear", key="clear_btn", use_container_width=True)
    with btn_col3:
        if st.button("🚀 Send Email", use_container_width=True):
            st.success("Email process initiated!")
