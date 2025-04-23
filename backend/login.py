import streamlit as st

USERS = {"1": "1"}

def login():
    st.markdown("<h1 style='text-align: center;'>🔐 Welcome to Vaylo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your AI-powered Compliance Companion</p>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("🚪 Login")

        if submitted:
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()
