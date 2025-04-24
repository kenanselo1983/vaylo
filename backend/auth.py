
# backend/auth.py

from supabase import create_client, Client
import streamlit as st


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]



supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_user(username, password, workspace):
    try:
        response = supabase.table("users").select("*").eq("username", username).eq("password", password).eq("workspace", workspace).execute()
        users = response.data
        if users and len(users) > 0:
            return True, users[0]["role"]
        else:
            return False, None
    except Exception as e:
        st.error(f"❌ Auth error: {e}")
        return False, None

def register_user(username, password, role, workspace):
    try:
        data = {
            "username": username,
            "password": password,
            "role": role,
            "workspace": workspace
        }
        supabase.table("users").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"❌ Registration error: {e}")
        return False

def get_all_users():
    try:
        result = supabase.table("users").select("*").execute()
        return result.data
    except Exception as e:
        st.error(f"❌ Fetching users failed: {e}")
        return []
