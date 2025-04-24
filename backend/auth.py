
# backend/auth.py

from supabase import create_client, Client
import streamlit as st

SUPABASE_URL = st.secrets["https://jfecmgsrzgkzecvnoecx.supabase.co"]
SUPABASE_KEY = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmZWNtZ3NyemdremVjdm5vZWN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0OTUwMzksImV4cCI6MjA2MTA3MTAzOX0.lUQcsmnwdVicjLefZnD9y8LEs68EGgw3u39YEfpbUzM"]

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
