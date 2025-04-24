from supabase import create_client
import os

SUPABASE_URL = "https://jfecmgsrzgkzecvnoecx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # full key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_user(username, password, workspace):
    response = supabase.table("users").select("*").eq("username", username).eq("password", password).eq("workspace", workspace).execute()
    users = response.data
    if users and len(users) > 0:
        return True, users[0]["role"]
    return False, None
