import streamlit as st
from backend.auth import register_user, get_all_users

def admin_panel():
    st.subheader("👑 Admin Panel – Manage Users")
    with st.form("create_user_form"):
        new_user = st.text_input("👤 Username", key="new_username")
        new_pass = st.text_input("🔑 Password", type="password", key="new_password")
        role = st.selectbox("🎓 Role", ["admin", "user"], key="new_role")
        workspace = st.text_input("🏢 Workspace", key="new_workspace")
        submit = st.form_submit_button("➕ Create User")

        if submit:
            success = register_user(new_user, new_pass, role, workspace)
            if success:
                st.success(f"✅ User '{new_user}' created!")
            else:
                st.error(f"❌ User '{new_user}' already exists.")

    st.markdown("---")
    st.subheader("👥 Existing Users")
    users = get_all_users()

    for user in users:
        try:
            st.write(f"👤 {user['username']} | Role: {user['role']} | Workspace: {user['workspace']}")
        except Exception as e:
            st.error(f"Error displaying user: {e}")
