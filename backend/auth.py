import os
from supabase import create_client, Client

# 🔐 Supabase credentials (move to env or Streamlit secrets in production)
SUPABASE_URL = "https://jfecmgsrzgkzecvnoecx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmZWNtZ3NyemdremVjdm5vZWN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0OTUwMzksImV4cCI6MjA2MTA3MTAzOX0.lUQcsmnwdVicjLefZnD9y8LEs68EGgw3u39YEfpbUzM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_user(username, password, workspace):
    try:
        result = supabase.table("users").select("*")\
            .eq("username", username)\
            .eq("password", password)\
            .eq("workspace", workspace).execute()
        if result.data:
            return True, result.data[0]["role"]
        return False, None
    except Exception as e:
        print("❌ Auth error:", e)
        return False, None

def register_user(username, password, role, workspace):
    try:
        response = supabase.table("users").insert({
            "username": username,
            "password": password,
            "role": role,
            "workspace": workspace
        }).execute()
        return True
    except Exception as e:
        print("❌ Registration error:", e)
        return False

def get_all_users():
    try:
        response = supabase.table("users").select("*").execute()
        return response.data
    except Exception as e:
        print("❌ Fetch users error:", e)
        return []

def authenticate_user(username, password, workspace):
    print(f"🔍 Authenticating: {username}, {password}, {workspace}")
    try:
        result = supabase.table("users").select("*").eq("username", username).eq("password", password).eq("workspace", workspace).execute()
        user = result.data[0] if result.data else None
        if user:
            return True, user["role"]
        return False, None
    except Exception as e:
        print(f"❌ Error authenticating: {e}")
        return False, None
