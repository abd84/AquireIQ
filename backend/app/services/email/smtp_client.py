import asyncio
import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "../../../../token.json")
_CREDS_PATH = os.path.join(os.path.dirname(__file__), "../../../../credentials.json")


def _get_gmail_service():
    if not os.path.exists(_TOKEN_PATH):
        raise RuntimeError(
            "Gmail not authorised. Run: python setup_gmail_auth.py"
        )
    creds = Credentials.from_authorized_user_file(_TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(_TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _send_sync(to_email: str, subject: str, body: str):
    service = _get_gmail_service()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg.attach(MIMEText(body, "plain"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()


async def send_outreach_email(to_email: str, subject: str, body: str):
    """Send via Gmail API (non-blocking)."""
    await asyncio.to_thread(_send_sync, to_email, subject, body)
