import os
import requests
import sys

# Credenciales desde GitHub Secrets
email = os.getenv('HG_EMAIL')
password = os.getenv('HG_PASSWORD')

def login():
    url = "https://dashboard.honeygain.com/api/v1/users/tokens"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['data']['access_token']
    else:
        print("❌ Login failed. Check your credentials.")
        sys.exit(1)

def claim_pot(token):
    url = "https://dashboard.honeygain.com/api/v1/contest_winnings"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("✅ Lucky Pot claimed successfully!")
        print(f"Result: {response.json()}")
    elif response.status_code == 401:
        print("❌ Token expired or invalid.")
    else:
        print(f"⚠️ Pot not available yet or already claimed. Response: {response.status_code}")

if __name__ == "__main__":
    if not email or not password:
        print("❌ Error: HG_EMAIL or HG_PASSWORD not found in Secrets.")
        sys.exit(1)
    
    access_token = login()
    claim_pot(access_token)