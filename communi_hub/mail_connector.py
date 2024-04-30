import base64
from email.message import EmailMessage
import datetime as dt
import os
from dotenv import set_key
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import pytz

import json

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CRED = json.loads(os.environ['CALENDAR_CRED'])

class MailConnector:
    def __init__(self) -> None:
        self.service = None
        self.creds = None
        self.connect_to_api()

    
    def connect_to_api(self):
        if os.path.exists("calendar_token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "calendar_token.json")

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(CRED, SCOPES)
                self.creds = flow.run_local_server(port=0)

        with open("calendar_token.json", "w") as token:
            token.write(self.creds.to_json())

        self.service = build("gmail", "v1", credentials=self.creds)
        print("Successfully connected to Google Gmail")

    def send_email(self, text_message, email):
        try:
            message = EmailMessage()

            message.set_content(text_message)
            time_utc = datetime.now(pytz.UTC).strftime("%d-%m-%Y %H:%M")

            
            message["To"] = email
            message["From"] = "gptintegration01@gmail.com"
            message["Subject"] = f"Mail {time_utc}"

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message