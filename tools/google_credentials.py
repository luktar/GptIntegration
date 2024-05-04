import datetime as dt
import os
from dotenv import set_key
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json


SCOPES = ["https://www.googleapis.com/auth/calendar", "https://mail.google.com/",
          "https://www.googleapis.com/auth/contacts.readonly"]
CRED = json.loads(os.environ['GOOGLE_CRED'])
TOKEN_FILE_NAME = "token.json"


class GoogleCredentials:
    def __init__(self):
        self.creds = None
        self.build_credentials()

    def build_credentials(self):
        if os.path.exists(TOKEN_FILE_NAME):
            self.creds = Credentials.from_authorized_user_file(
                TOKEN_FILE_NAME)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(CRED, SCOPES)
                self.creds = flow.run_local_server(port=0)
                
        with open(TOKEN_FILE_NAME, "w") as token:
            token.write(self.creds.to_json())
