from supabase import create_client, Client

SUPABASE_URL = "https://jfecmgsrzgkzecvnoecx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpmZWNtZ3NyemdremVjdm5vZWN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0OTUwMzksImV4cCI6MjA2MTA3MTAzOX0.lUQcsmnwdVicjLefZnD9y8LEs68EGgw3u39YEfpbUzM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_user(username, password, workspace):
    response = supabase.table("users").select("role").eq("username", username).eq("password", password).eq("workspace", workspace).execute()
    if response.data and len(response.data) > 0:
        return True, response.data[0]["role"]
    return False, None

def register_user(username, password, role, workspace):
    existing = supabase.table("users").select("id").eq("username", username).execute()
    if existing.data:
        return False
    supabase.table("users").insert({
        "username": username,
        "password": password,
        "role": role,
        "workspace": workspace
    }).execute()
    return True

def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data if response.data else []
