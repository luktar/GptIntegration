import datetime as dt
import os.path
from dotenv import set_key
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class CalendarConnector:
    def __init__(self):
        self.creds=None
        self.service=None
        self.connect_to_api()
        self.create_service()
    
    def connect_to_api(self):    
        if os.path.exists("token.json"):
            self.creds=Credentials.from_authorized_user_file("token.json")
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(self.creds.to_json())
    
    def create_service(self):
        self.service = build("calendar", "v3", credentials=self.creds)
        print("Successfully connected to Google Calendar")
        
    def add_appointment_to_calendar(self, appointment_title: str, appointment_date: str):
        try: 
            if dt.datetime.strptime(appointment_title, "%Y-%m-%d").date() < dt.datetime.now().date():
                print("You can only create events for today or future dates")
                return
            
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
            
            event =self.service.events().insert(calendarId="primary", body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
    
    def del_appoinment_from_calendar(self, appointment_title: str, appointment_date: str):
        try:
            start = f"{appointment_date}T08:00:00+02:00"
            end = f"{appointment_date}T10:00:00+02:00"
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start,
                timeMax=end,
                q=appointment_title,
                maxResults=1
            ).execute()

            if not events_result.get('items', []):
                print("No events found.")
                return
            
            for event in events_result.get('items', []):
                event_id = event['id']
                self.service.events().delete(calendarId='primary', eventId=event_id).execute()
                print(f"Deleted event with title '{appointment_title}' at {start}.")
                
        except HttpError as error:
            print(f"An error occurred: {error}")
    

if __name__ == "__main__":
    calendar=CalendarConnector()
    #calendar.add_appointment_to_calendar("Meeting test", "2024-05-01")
    calendar.del_appoinment_from_calendar("Meeting test", "2024-05-01")