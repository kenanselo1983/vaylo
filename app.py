import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from backend.rule_engine import evaluate_data, load_rules
from backend.scanner import fetch_data_from_db
from backend.pdf_exporter import generate_html_report
from backend.law_watcher import fetch_kvkk_updates, summarize

# --- Basic login ---
USERS = {"1": "1"}

def login():
    st.title("🔐 Vaylo Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    login()
    st.stop()

st.title("📋 Vaylo – Compliance Scanner")
st.caption(f"👤 Logged in as: {st.session_state.user}")
st.button("Logout", on_click=logout)

option = st.radio("Choose data source:", ["Upload CSV", "Scan Local Database"])
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

if records:
    kvkk = load_rules("backend/rules/kvkk_rules.json")
    gdpr = load_rules("backend/rules/gdpr_rules.json")
    rules = kvkk + gdpr
    results = evaluate_data(records, rules)

    st.subheader("🔍 Violations")
    if results:
        df_results = pd.DataFrame(results)
        st.dataframe(df_results)
    else:
        st.success("🎉 No violations found!")

    # Generate and show HTML report
    html_data = generate_html_report(results)
    st.subheader("🧾 Compliance Report (HTML View)")
    components.html(html_data.decode("utf-8"), height=600, scrolling=True)

    # Allow download
    st.download_button(
        label="💾 Download HTML Report",
        data=html_data,
        file_name="vaylo_report.html",
        mime="text/html",
    )

st.markdown("---")
st.subheader("🧠 KVKK Update Summary (Mock)")

if st.button("Fetch KVKK Summary"):
    with st.spinner("Fetching and summarizing KVKK page..."):
        content = fetch_kvkk_updates()
        summary = summarize(content)
        st.success("Done!")
        st.text_area("📝 GPT Summary:", summary, height=200)
