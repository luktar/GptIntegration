import datetime as dt
import os
from dotenv import set_key
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalendarConnector:

    def __init__(self, calendar_cred):
        self.service = None
        self.connect_to_api(calendar_cred)

    def connect_to_api(self, calendar_cred):
        flow = InstalledAppFlow.from_client_config(calendar_cred, SCOPES)
        creds = flow.run_local_server(port=0)

        self.service = build("calendar", "v3", credentials=creds)
        print("Successfully connected to Google Calendar")

    def add_appointment_to_calendar(self, appointment_title: str, appointment_date: str):
        try:
            if dt.datetime.strptime(appointment_date, "%Y-%m-%d").date() < dt.datetime.now().date():
                return "You can only create events for today or future dates"

            event = {
                "summary": appointment_title,
                "colorId": 2,
                "start": {
                    "dateTime": f"{appointment_date}T08:00:00+02:00",
                    "timeZone": "Europe/Warsaw",
                },
                "end": {
                    "dateTime": f"{appointment_date}T10:00:00+02:00",
                    "timeZone": "Europe/Warsaw",
                }
            }

            event = self.service.events().insert(calendarId="primary", body=event).execute()
            return f"Event created successfully {event.get('htmlLink')}"

        except HttpError as error:
            return "Error occurred while adding appointment to calendar."

    def delete_appointment_from_calendar(self, appointment_date: str):
        try:
            start = f"{appointment_date}T01:00:00+02:00"
            end = f"{appointment_date}T20:00:00+02:00"

            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start,
                timeMax=end,
                maxResults=2,
            ).execute()

            if not events_result.get('items', []):
                return f"No events found on {appointment_date}"

            for event in events_result.get('items', []):
                event_id = event['id']
                self.service.events().delete(calendarId='primary', eventId=event_id).execute()
                return f"Deleted event on {appointment_date}."

        except HttpError as error:
            return "Error occurred while deleting appointment from calendar."
