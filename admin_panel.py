import streamlit as st
from backend.auth import register_user, get_all_users

def admin_panel():
    st.header("👑 Admin Panel – Manage Users")

    with st.expander("➕ Create New User"):
        new_username = st.text_input("👤 Username", key="admin_username")
        new_password = st.text_input("🔑 Password", type="password", key="admin_password")
        new_role = st.selectbox("🎓 Role", ["user", "admin"], key="admin_role")

        if st.button("✅ Register User", key="admin_register"):
            workspace = st.session_state.workspace
            success = register_user(new_username, new_password, new_role, workspace)
            if success:
                st.success(f"✅ User '{new_username}' created.")
            else:
                st.error(f"❌ User '{new_username}' already exists.")

    st.divider()
    st.subheader("👥 Existing Users")
    users = get_all_users()
    if users:
        for user in users:
            st.write(f"👤 {user['username']} | Role: {user['role']} | Workspace: {user['workspace']}")
    else:
        st.info("No users found.")
