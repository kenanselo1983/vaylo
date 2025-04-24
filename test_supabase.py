from supabase import create_client, Client
import os

SUPABASE_URL = "https://jfecmgsrzgkzecvnoecx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmZWNtZ3NyemdremVjdm5vZWN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0OTUwMzksImV4cCI6MjA2MTA3MTAzOX0.lUQcsmnwdVicjLefZnD9y8LEs68EGgw3u39YEfpbUzM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔍 Try reading from "users" table
try:
    response = supabase.table("users").select("*").limit(5).execute()
    print("✅ Connected successfully. Users table:")
    for user in response.data:
        print(user)
except Exception as e:
    print("❌ Error:", e)
