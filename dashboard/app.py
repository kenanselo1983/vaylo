import streamlit as st
import pandas as pd
from backend.rule_engine import evaluate_data, load_rules
from backend.scanner import fetch_data_from_db
from backend.pdf_exporter import generate_pdf_report

st.set_page_config(page_title="Vaylo", layout="wide")
st.title("📋 Vaylo – Compliance Scanner")

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
