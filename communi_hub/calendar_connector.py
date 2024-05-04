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
from tools.google_credentials import GoogleCredentials

dotenv_path = Path('../.env')
load_dotenv()


class CalendarConnector:

    def __init__(self):
        self.google_credentials = GoogleCredentials()
        self.calendar_service = None
        self.initialize_service()

    def initialize_service(self):
        self.calendar_service = build(
            "calendar", "v3", credentials=self.google_credentials.creds)
        print("Successfully connected to Google Calendar")

    def add_appointment_to_calendar(self, appointment_title: str, appointment_date: str, appointment_hour: str):
        print(appointment_date)
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
            return f"Wydarzenie zostało utworzone. Data: {appointment_date} {appointment_hour}"

        except HttpError as error:
            return "Error occurred while adding appointment to calendar."

    def delete_appointment_from_calendar(self, appointment_date: str, appointment_hour: str):
        if not self.calendar_service:
            self.connect_to_api()
        try:
            start_time_appointment = f"{appointment_date}T{appointment_hour}:00:00"
            start_time = datetime.fromisoformat(start_time_appointment)
            finish_time = start_time + timedelta(hours=1)
            finish_time_appointment = finish_time.isoformat()
            start_time_appointment = start_time_appointment + self.create_time_zone()
            finish_time_appointment = finish_time_appointment + self.create_time_zone()
            print(start_time_appointment, finish_time_appointment)
            events_result = self.calendar_service.events().list(
                calendarId='primary',
                timeMax=finish_time_appointment,
                timeMin=start_time_appointment,
            ).execute()

            if not events_result.get('items', []):
                return f"You can't delete event what not exist in calendar on {appointment_date}"

            for event in events_result.get('items', []):
                event_id = event['id']
                self.calendar_service.events().delete(
                    calendarId='primary', eventId=event_id).execute()
                return f"Deleted event on {appointment_date}."

        except HttpError as error:
            return f"Error occurred while deleting appointment from calendar. {error}"

    def create_time_zone(self):
        current_timezone_offset = datetime.now(
            timezone.utc).astimezone().utcoffset()

        hours_offset = current_timezone_offset.total_seconds() // 3600
        minutes_offset = (current_timezone_offset.total_seconds() % 3600) // 60

        timezone_offset_text = f"{int(hours_offset):+03d}:{int(minutes_offset):02d}"

        return timezone_offset_text
