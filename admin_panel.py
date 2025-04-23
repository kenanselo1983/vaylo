""import streamlit as st
import sqlite3
from backend.auth import register_user, get_all_users

def admin_panel():
    st.title("👑 Admin Panel – Manage Users")
    st.subheader("➕ Create New User")

    with st.form("admin-user-form", clear_on_submit=True):
        new_user = st.text_input("👤 Username")
        new_pass = st.text_input("🔑 Password", type="password")
        first_name = st.text_input("🧍 First Name")
        last_name = st.text_input("👥 Last Name")
        email = st.text_input("📧 Email")
        phone = st.text_input("📞 Phone Number")
        role = st.selectbox("🎓 Role", ["admin", "user"])
        submitted = st.form_submit_button("✅ Register")

        if submitted:
            success = register_user(
                username=new_user,
                password=new_pass,
                role=role,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                workspace=st.session_state.workspace
            )
            if success:
                st.success(f"✅ User '{new_user}' registered successfully.")
            else:
                st.error(f"❌ User '{new_user}' already exists.")

    st.markdown("---")
    st.subheader("👥 Existing Users")

    users = get_all_users()
    for user in users:
        st.write(f"👤 {user[0]} | Role: {user[2]} | Workspace: {user[3]}")
