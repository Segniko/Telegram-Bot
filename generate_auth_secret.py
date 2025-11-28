import base64
import os

AUTH_FILE = 'auth.json'

def generate_secret():
    if not os.path.exists(AUTH_FILE):
        print(f"❌ Error: {AUTH_FILE} not found!")
        print("Please run 'python login.py' first.")
        return

    with open(AUTH_FILE, 'rb') as f:
        auth_content = f.read()
    
    # Encode to base64
    encoded = base64.b64encode(auth_content).decode('utf-8')
    
    print("="*60)
    print("🔐 GitHub Secret Generator")
    print("="*60)
    print("Create a new secret in your GitHub Repo settings:")
    print("Name:  TWITTER_AUTH")
    print("Value: (Copy the string below)")
    print("-" * 60)
    print(encoded)
    print("-" * 60)
    print("⚠️  Keep this secret safe! Do not share it.")

if __name__ == "__main__":
    generate_secret()
