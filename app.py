print('✅ THIS IS THE REAL app.py BEING READ')

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from backend.rule_engine import evaluate_data, load_rules
from backend.scanner import fetch_data_from_db
from backend.pdf_exporter import generate_html_report
from backend.law_watcher import summarize
from backend.scraper import fetch_kvkk_updates
from backend.chatbot import ask_chatbot
from backend.suggestions import suggest_fixes
from backend.risk import calculate_risk_score, explain_risk_with_ai
from backend.doc_reader import extract_text_from_docx, extract_text_from_txt
from backend.policy_ai import summarize_policy
from backend.google_loader import load_google_sheet
from backend.login import login_form
from backend.login import login


st.markdown(f"👤 Logged in as: `{st.session_state.user}`")
st.button("🚪 Logout", on_click=logout)




# Session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.workspace = None

if not st.session_state.logged_in:
    login_form()
    st.stop()

# Top UI
st.title("📋 Vaylo – Compliance Scanner")
st.caption(f"👤 Logged in as: {st.session_state.user} ({st.session_state.role}) – Workspace: {st.session_state.workspace}")
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.workspace = None

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.workspace = None
    st.rerun()

def login_ui():
    st.title("🔐 Vaylo Workspace Login")
    with st.form("login_form"):
        workspace = st.text_input("🏢 Workspace Code")
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            success, role = authenticate_user(username, password, workspace)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.workspace = workspace
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Login failed. Check credentials or workspace code.")

# Redirect to login if not authenticated
if not st.session_state.logged_in:
    login_ui()
    st.stop()

# After login
st.sidebar.success(f"👤 {st.session_state.username} | 🏢 {st.session_state.workspace} | 🎓 {st.session_state.role}")
st.sidebar.button("🚪 Logout", on_click=logout)







from admin_panel import admin_panel

st.title("📋 Vaylo Compliance Dashboard")
st.caption(f"Welcome {st.session_state.username} from workspace '{st.session_state.workspace}'")

# Role-based routing
if st.session_state.role == "admin":
    tab = st.sidebar.radio("📂 Admin Navigation", ["Dashboard", "User Management"])
    if tab == "Dashboard":
        st.header("📊 Compliance Scanner")
        # Place your main dashboard logic here (scanner, uploads, etc.)
    elif tab == "User Management":
        admin_panel()
else:
    st.header("📊 Compliance Scanner")
    # Place your main dashboard logic here




# -------- DATA SOURCE OPTIONS --------
option = st.radio("Choose data source:", ["Upload CSV", "Scan Local Database", "Google Sheets"])
records = []

# Upload CSV
if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} records.")
        st.dataframe(df)
        records = df.to_dict(orient="records")

# Scan Local Database
elif option == "Scan Local Database":
    try:
        records = fetch_data_from_db()
        st.success(f"✅ Fetched {len(records)} records from local DB.")
        st.dataframe(pd.DataFrame(records))
    except Exception as e:
        st.error(f"❌ Error fetching from DB: {e}")

# Google Sheets
elif option == "Google Sheets":
    st.subheader("📄 Load Data from Google Sheets")
    st.info("✅ Make sure the sheet is public and ends with `/gviz/tq?tqx=out:csv`")

    sheet_url = st.text_input(
        "Paste your Google Sheets CSV link",
        value="https://docs.google.com/spreadsheets/d/10DReLchE2zNPvbqEIf19XU69lpni_0-w1NTOBFnhN34/gviz/tq?tqx=out:csv"
    )

    if sheet_url:
        try:
            df = pd.read_csv(sheet_url)
            st.success(f"✅ Loaded {len(df)} rows from Google Sheets.")
            st.dataframe(df)
            records = df.to_dict(orient="records")
        except Exception as e:
            st.error(f"❌ Could not load data from Google Sheets.\n\n**{type(e).__name__}:** {e}")

# -------- SCANNING --------
if records:
    kvkk = load_rules("backend/rules/kvkk_rules.json")
    gdpr = load_rules("backend/rules/gdpr_rules.json")
    rules = kvkk + gdpr
    results = evaluate_data(records, rules)

    score = calculate_risk_score(results)
    color = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"
    st.subheader(f"🧮 Risk Score: {score}/100 {color}")

    if st.button("🧠 Explain Risk Score"):
        explanation = explain_risk_with_ai(score, results)
        st.text_area("📋 Risk Summary", explanation, height=300)

    st.subheader("🔍 Violations")
    if results:
        df_results = pd.DataFrame(results)
        st.dataframe(df_results)

        if st.button("💡 Suggest Compliance Improvements"):
            suggestions = suggest_fixes(results)
            st.text_area("🧠 AI Suggestions", suggestions, height=300)

        html_data = generate_html_report(results)
        st.subheader("🧾 Compliance Report (HTML View)")
        components.html(html_data.decode("utf-8"), height=600, scrolling=True)
        st.download_button(
            label="💾 Download HTML Report",
            data=html_data,
            file_name="vaylo_report.html",
            mime="text/html",
        )
    else:
        st.success("🎉 No violations found!")

# -------- POLICY AI --------
st.markdown("---")
st.subheader("📄 Upload Privacy Policy (.docx or .txt)")

uploaded_policy = st.file_uploader("Upload your policy file", type=["docx", "txt"])
if uploaded_policy:
    with st.spinner("Reading file..."):
        if uploaded_policy.type == "text/plain":
            policy_text = extract_text_from_txt(uploaded_policy)
        else:
            policy_text = extract_text_from_docx(uploaded_policy)

        st.text_area("📖 Extracted Policy Text", policy_text, height=200)

    if st.button("🧠 Summarize and Suggest"):
        with st.spinner("Thinking..."):
            result = summarize_policy(policy_text)
            st.success("✅ Summary and suggestions ready:")
            st.text_area("📋 Policy AI Output", result, height=300)

# -------- KVKK UPDATE --------
st.markdown("---")
st.subheader("🧠 KVKK Update Summary (AI-Powered)")

if st.button("Fetch KVKK Summary"):
    with st.spinner("Fetching and summarizing latest KVKK content..."):
        text = fetch_kvkk_updates()
        st.text_area("📄 Raw KVKK Text", text, height=200)
        summary = summarize(text)
        st.success("✅ AI summary complete")
        st.text_area("📄 Summary", summary, height=300)

# -------- CHATBOT --------
st.markdown("---")
st.subheader("💬 KVKK/GDPR Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a legal assistant specialized in Turkish KVKK and GDPR. Respond clearly in Turkish or English depending on the user's question. Use bullet points when needed."}
    ]

user_input = st.chat_input("Ask a KVKK or GDPR question in English or Turkish...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Yanıt hazırlanıyor..."):
            answer = ask_chatbot(st.session_state.chat_history)
            st.markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

elif option == "Load from Google Sheet":
    sheet_url = st.text_input(
        "Paste Google Sheet CSV URL",
        value="https://docs.google.com/spreadsheets/d/10DReLchE2zNPvbqEIf19XU69lpni_0-w1NTOBFnhN34/gviz/tq?tqx=out:csv"
    )

    if st.button("🔄 Load Google Sheet"):
        records = load_google_sheet(sheet_url)
        if records:
            st.success(f"✅ Loaded {len(records)} rows from Google Sheet.")
            st.dataframe(pd.DataFrame(records))
        else:
            st.error("❌ Couldn’t load sheet. Make sure it’s public and the URL is correct.")

option = st.radio("Choose data source:", ["Upload CSV", "Scan Local Database", "Google Sheet"])
records = []

if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df)} records.")
        st.dataframe(df)
        records = df.to_dict(orient="records")

elif option == "Scan Local Database":
    try:
        records = fetch_data_from_db()
        st.success(f"Fetched {len(records)} records from company_data.db")
        st.dataframe(pd.DataFrame(records))
    except Exception as e:
        st.error(f"Error fetching data: {e}")

elif option == "Google Sheet":
    sheet_url = st.text_input("Paste Google Sheet URL", value="https://docs.google.com/spreadsheets/d/10DReLchE2zNPvbqEIf19XU69lpni_0-w1NTOBFnhN34/gviz/tq?tqx=out:csv")
    if sheet_url:
        try:
            df = load_google_sheet(sheet_url)
            st.success(f"Loaded {len(df)} rows from Google Sheet.")
            st.dataframe(df)
            records = df.to_dict(orient="records")
        except Exception as e:
            st.error(f"❌ Could not load data. Check the sheet URL.\n\n{e}")

if records:
    kvkk = load_rules("backend/rules/kvkk_rules.json")
    gdpr = load_rules("backend/rules/gdpr_rules.json")
    rules = kvkk + gdpr
    results = evaluate_data(records, rules)

    score = calculate_risk_score(results)
    color = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"
    st.subheader(f"🧮 Risk Score: {score}/100 {color}")

    if st.button("🧠 Explain Risk Score"):
        with st.spinner("Generating explanation..."):
            explanation = explain_risk_with_ai(score, results)
            st.text_area("📋 Risk Summary", explanation, height=300)

    st.subheader("🔍 Violations")
    if results:
        df_results = pd.DataFrame(results)
        st.dataframe(df_results)

        if st.button("💡 Suggest Compliance Improvements"):
            with st.spinner("Analyzing violations..."):
                suggestions = suggest_fixes(results)
                st.success("✅ Suggestions ready:")
                st.text_area("🧠 AI Suggestions", suggestions, height=300)

        html_data = generate_html_report(results)
        st.subheader("🧾 Compliance Report (HTML View)")
        components.html(html_data.decode("utf-8"), height=600, scrolling=True)
        st.download_button(
            label="💾 Download HTML Report",
            data=html_data,
            file_name="vaylo_report.html",
            mime="text/html",
        )
    else:
        st.success("🎉 No violations found!")

st.markdown("---")
st.subheader("📄 Upload Privacy Policy (.docx or .txt)")

uploaded_policy = st.file_uploader("Upload your policy file", type=["docx", "txt"])
if uploaded_policy:
    with st.spinner("Reading file..."):
        if uploaded_policy.type == "text/plain":
            policy_text = extract_text_from_txt(uploaded_policy)
        else:
            policy_text = extract_text_from_docx(uploaded_policy)

        st.text_area("📖 Extracted Policy Text", policy_text, height=200)

    if st.button("🧠 Summarize and Suggest"):
        with st.spinner("Thinking..."):
            result = summarize_policy(policy_text)
            st.success("✅ Summary and suggestions ready:")
            st.text_area("📋 Policy AI Output", result, height=300)

st.markdown("---")
st.subheader("🧠 GDPR / Compliance Update Summary (AI-Powered)")

if st.button("Fetch Legal Summary"):
    with st.spinner("Fetching and summarizing legal content..."):
        text = fetch_kvkk_updates()
        st.text_area("📄 Raw Text", text, height=200)
        summary = summarize(text)
        st.success("✅ AI summary complete")
        st.text_area("📄 Summary", summary, height=300)

st.markdown("---")
st.subheader("💬 GDPR Chatbot Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a compliance assistant specialized in GDPR and industry regulations. Respond clearly in English or Turkish."}
    ]

user_input = st.chat_input("Ask a compliance question...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Preparing response..."):
            answer = ask_chatbot(st.session_state.chat_history)
            st.markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
