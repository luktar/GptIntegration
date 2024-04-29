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
from datetime import datetime, timedelta, timezone

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

    def add_appointment_to_calendar(self, appointment_title: str, appointment_date: str, appointment_hour: str):
        if not self.service:
            self.connect_to_api()
    
        start_time_appointment = f"{appointment_date}T{appointment_hour}:00:00"
        start_time = datetime.fromisoformat(start_time_appointment)
        finish_time = start_time + timedelta(hours=1)
        finish_time_appointment = finish_time.isoformat()
        
        try:
            if dt.datetime.strptime(appointment_date, "%Y-%m-%d").date() < dt.datetime.now().date():
                return "You can only create events for today or future dates"

            event = {
                "summary": appointment_title,
                "colorId": 2,
                "start": {
                    "dateTime": f"{start_time_appointment}",
                    "timeZone": "Europe/Warsaw",
                },
                "end": {
                    "dateTime": f"{finish_time_appointment}",
                    "timeZone": "Europe/Warsaw",
                }
            }

            event = self.service.events().insert(calendarId="primary", body=event).execute()
            return f"Event created successfully {event.get('htmlLink')}"

        except HttpError as error:
            return "Error occurred while adding appointment to calendar."

    def delete_appointment_from_calendar(self, appointment_date: str, appointment_hour: str):
        if not self.service:
            self.connect_to_api()
        try:
            start_time_appointment = f"{appointment_date}T{appointment_hour}:00:00"
            start_time = datetime.fromisoformat(start_time_appointment)
            finish_time = start_time + timedelta(hours=1)
            finish_time_appointment = finish_time.isoformat()
            start_time_appointment = start_time_appointment + self.create_time_zone()
            finish_time_appointment = finish_time_appointment + self.create_time_zone()
            print(start_time_appointment, finish_time_appointment)
            events_result = self.service.events().list(
                calendarId='primary',
                timeMax=finish_time_appointment,
                timeMin=start_time_appointment,
            ).execute()

            if not events_result.get('items', []):
                return f"No events found on {appointment_date}"

            for event in events_result.get('items', []):
                event_id = event['id']
                self.service.events().delete(calendarId='primary', eventId=event_id).execute()
                return f"Deleted event on {appointment_date}."

        except HttpError as error:
            return f"Error occurred while deleting appointment from calendar. {error}"
        
    def create_time_zone(self):
        current_timezone_offset = datetime.now(timezone.utc).astimezone().utcoffset()

        hours_offset = current_timezone_offset.total_seconds() // 3600
        minutes_offset = (current_timezone_offset.total_seconds() % 3600) // 60

        timezone_offset_text = f"{int(hours_offset):+03d}:{int(minutes_offset):02d}"

        return timezone_offset_text

