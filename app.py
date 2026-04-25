import streamlit as st
import pandas as pd
import time
import json
from fpdf import FPDF
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="AegisFlow SOC | Agentic AI Demo", layout="wide")

# --- MOCK INFRASTRUCTURE STATE ---
if 'firewall_blocked' not in st.session_state:
    st.session_state.firewall_blocked = []
if 'disabled_users' not in st.session_state:
    st.session_state.disabled_users = []
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- STYLES ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stAlert { border-radius: 10px; }
    .agent-brain { 
        background-color: #1e1e1e; 
        color: #00ff00; 
        padding: 15px; 
        border-radius: 5px; 
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Control Center ---
st.sidebar.title("🛡️ AegisFlow Control")
mode = st.sidebar.selectbox("Operation Mode", ["Simulated (Demo Mode)", "Live (AWS/Panorama)"])
st.sidebar.info(f"System Status: **Active**\n\nAgent: **Claude-3-Sonnet**")

# --- APP LAYOUT ---
st.title("AegisFlow: Autonomous Cloud & Network Security")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚨 Real-Time Threat Feed")
    
    # Pre-defined Threats for Demo
    threat_choice = st.selectbox("Select a Threat Scenario to Inject:", [
        "Brute Force Attack (Network)",
        "Unauthorized S3 Exfiltration (Cloud)",
        "Compromised Admin Credentials (IAM)"
    ])
    
    if st.button("Inject Threat"):
        if "Brute Force" in threat_choice:
            st.session_state.current_threat = {"id": "EVT-992", "type": "Network Intrusion", "ip": "192.168.44.10", "severity": 8.5}
        elif "S3" in threat_choice:
            st.session_state.current_threat = {"id": "EVT-104", "type": "Data Exfiltration", "user": "dev-user-04", "severity": 7.2}
        else:
            st.session_state.current_threat = {"id": "EVT-501", "type": "IAM Compromise", "user": "admin-global", "severity": 9.8}
        st.warning(f"NEW CRITICAL ALERT: {st.session_state.current_threat['type']}")

with col2:
    st.subheader("🧠 Agent Reasoning (The 'Brain')")
    log_area = st.empty()
    if 'current_threat' in st.session_state:
        with st.container():
            t = st.session_state.current_threat
            
            # Step 1: Thought Process
            st.write(f"**Step 1: Analyzing {t['id']}...**")
            time.sleep(1)
            st.markdown(f"<div class='agent-brain'>[THOUGHT] Severity is {t['severity']}. This exceeds autonomous threshold. Requesting human-in-the-loop approval for isolation.</div>", unsafe_allow_html=True)
            
            # Step 2: Human in the Loop
            st.write("---")
            st.write("### 🛑 Action Required")
            st.write(f"The Agent wants to isolate **{t.get('ip') or t.get('user')}**.")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Authorize Action", key="auth"):
                    # Step 3: Execution
                    st.success("Authorization Received.")
                    st.markdown("<div class='agent-brain'>[ACTION] Calling Panorama API / AWS IAM SDK...<br>[VERIFICATION] Checking state... Success.</div>", unsafe_allow_html=True)
                    
                    if 'ip' in t: st.session_state.firewall_blocked.append(t['ip'])
                    if 'user' in t: st.session_state.disabled_users.append(t['user'])
                    
                    # Step 4: Report Generation
                    st.write("---")
                    st.write("### 📄 Audit Report Generated")
                    
                    # Simple PDF Generate logic
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt="AegisFlow Remediation Report", ln=True, align='C')
                    pdf.cell(200, 10, txt=f"Threat: {t['type']} | Status: MITIGATED", ln=True)
                    pdf_output = f"Report_{t['id']}.pdf"
                    pdf.output(pdf_output)
                    
                    with open(pdf_output, "rb") as f:
                        st.download_button("Download Compliance PDF", f, file_name=pdf_output)
            
            with col_b:
                if st.button("❌ Deny & Ignore"):
                    st.error("Action Aborted by Operator.")

# --- FOOTER: Infrastructure State ---
st.write("---")
st.subheader("🌐 Current Infrastructure State")
st_col1, st_col2 = st.columns(2)
with st_col1:
    st.write("**Panorama IP Quarantine List**")
    st.write(st.session_state.firewall_blocked if st.session_state.firewall_blocked else "No active blocks.")
with st_col2:
    st.write("**AWS IAM Disabled Users**")
    st.write(st.session_state.disabled_users if st.session_state.disabled_users else "No disabled users.")
