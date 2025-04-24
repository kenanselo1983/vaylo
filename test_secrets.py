import streamlit as st

st.write("SUPABASE_URL:", st.secrets.get("SUPABASE_URL"))
st.write("SUPABASE_KEY:", st.secrets.get("SUPABASE_KEY"))
