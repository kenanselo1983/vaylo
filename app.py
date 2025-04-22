import streamlit as st
import pandas as pd
from backend.rule_engine import evaluate_data, load_rules
from backend.scanner import fetch_data_from_db
from backend.pdf_exporter import generate_pdf_report
from backend.law_watcher import fetch_kvkk_updates, summarize

# --- Mock user database ---
USERS = {
    "admin@example.com": "admin123",
    "legal@company.com": "legalpass",
    "test@vaylo.ai": "test"
}

def login():
    st.title("🔐 Vaylo Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email in USERS and USERS[email] == password:
            st.session_state.logged_in = True
            st.session_state.user = email
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.experimental_rerun()

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

        csv = df_results.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Violations Report (CSV)",
            data=csv,
            file_name="vaylo_violations_report.csv",
            mime="text/csv",
        )

        pdf_data = generate_pdf_report(results)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name="vaylo_report.pdf",
            mime="application/pdf",
        )
    else:
        st.success("🎉 No violations found!")

st.markdown("---")
st.subheader("🧠 KVKK Update Summary (Mock)")

if st.button("Fetch KVKK Summary"):
    with st.spinner("Fetching and summarizing KVKK page..."):
        content = fetch_kvkk_updates()
        summary = summarize(content)
        st.success("Done!")
        st.text_area("📝 GPT Summary:", summary, height=200)
