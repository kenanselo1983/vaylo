import streamlit as st
import sqlite3
from backend.auth import authenticate_user

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

def logout():
    st.session_state.clear()
    st.rerun()
