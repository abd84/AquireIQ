"""
Run this ONCE to authorize Gmail access.
It opens a browser, you log in, then saves token.json.
After that the app sends emails without any user interaction.

Usage:
    cd backend
    python setup_gmail_auth.py
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

with open("token.json", "w") as f:
    f.write(creds.to_json())

print("✓ token.json saved — Gmail sending is now configured.")
