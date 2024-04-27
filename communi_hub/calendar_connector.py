import datetime as dt
import os
from dotenv import set_key
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CRED = json.loads(os.environ['CALENDAR_CRED'])


class CalendarConnector:

    def __init__(self):
        self.service = None
        self.creds = None
        self.connect_to_api()

    # Wersja bez tokenu w json
    # def connect_to_api(self):
    #     flow = InstalledAppFlow.from_client_config(CRED, SCOPES)
    #     self.creds = flow.run_local_server(port=0)
    #     self.service = build("calendar", "v3", credentials=self.creds)
    #     print("Successfully connected to Google Calendar")

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

        self.service = build("calendar", "v3", credentials=self.creds)
        print("Successfully connected to Google Calendar")

    def add_appointment_to_calendar(self, appointment_title: str, appointment_date: str):
        if not self.service:
            self.connect_to_api()
        try:
            if dt.datetime.strptime(appointment_date, "%Y-%m-%d").date() < dt.datetime.now().date():
                return "You can only create events for today or future dates"

            event = {
                "summary": appointment_title,
                "colorId": 2,
                "start": {
                    "dateTime": f"{appointment_date}T08:00:00Z",
                    "timeZone": "Europe/Warsaw",
                },
                "end": {
                    "dateTime": f"{appointment_date}T10:00:00Z",
                    "timeZone": "Europe/Warsaw",
                }
            }

            event = self.service.events().insert(calendarId="primary", body=event).execute()
            return f"Event created successfully {event.get('htmlLink')}"

        except HttpError as error:
            return "Error occurred while adding appointment to calendar."

    def delete_appointment_from_calendar(self, appointment_date: str):
        if not self.service:
            self.connect_to_api()
        try:
            start = f"{appointment_date}T08:00:00Z"
            end = f"{appointment_date}T10:00:00Z"

            events_result = self.service.events().list(
                calendarId='primary',
                timeMax=end,
                timeMin=start,
            ).execute()

            if not events_result.get('items', []):
                return f"No events found on {appointment_date}"

            for event in events_result.get('items', []):
                event_id = event['id']
                self.service.events().delete(calendarId='primary', eventId=event_id).execute()
                return f"Deleted event on {appointment_date}."

        except HttpError as error:
            return "Error occurred while deleting appointment from calendar."
