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
from tools.google_credentials import GoogleCredentials

class MailConnector:
    def __init__(self) -> None:
        self.gmail_service = None
        self.contacts_service = None
        self.google_credentials = GoogleCredentials()
        self.initialize_service()

    def initialize_service(self):
        self.gmail_service = build("gmail", "v1", credentials=self.google_credentials.creds)
        print("Successfully connected to Google Gmail")
        self.contacts_service = build('people', 'v1', credentials=self.google_credentials.creds)
        print("Successfully connected to Google Contacts")
        
    def get_contacts(self):
        results = self.contacts_service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,emailAddresses').execute()
        connections = results.get('connections', [])

        result = []
        for person in connections:
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                emails = person.get('emailAddresses', [])
                if emails:
                    email = emails[0].get('value')
                    result.append(f"Name: {name}, Email: {email}")
        return ", ".join(result)

    def send_email(self, text_message, email):
        try:
            if (not email or "example" in email):
                return f"Niepoprawny adres email {email}"

            message = EmailMessage()

            message.set_content(text_message)
            time_utc = datetime.now(pytz.UTC).strftime("%d-%m-%Y %H:%M")

            message["To"] = email
            message["From"] = "gptintegration01@gmail.com"
            message["Subject"] = f"Mail {time_utc}"

            # encoded message
            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
                self.gmail_service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = "Błąd wysyłania wiadomości"
        return f"Wiadomość została wysłana na adres {email}"
