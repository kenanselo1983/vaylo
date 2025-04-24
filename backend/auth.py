
# backend/auth.py

from supabase import create_client
import os

SUPABASE_URL = os.getenv("https://jfecmgsrzgkzecvnoecx.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmZWNtZ3NyemdremVjdm5vZWN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0OTUwMzksImV4cCI6MjA2MTA3MTAzOX0.lUQcsmnwdVicjLefZnD9y8LEs68EGgw3u39YEfpbUzM")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_user(username, password, workspace):
    try:
        print(f"🔍 Checking user: {username}, workspace: {workspace}")
        result = supabase.table("users").select("*").eq("username", username).eq("password", password).eq("workspace", workspace).execute()

        if result.data:
            role = result.data[0]["role"]
            print(f"✅ Auth success: role = {role}")
            return True, role
        else:
            print("❌ No user found")
            return False, None

    except Exception as e:
        print(f"❌ Supabase error: {e}")
        return False, None
