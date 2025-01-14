import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def create_google_calendar_event(event_data, calendar_id="primary"):
    try:
        service = get_google_calendar_service()

        start_time = datetime.fromisoformat(event_data["start_time"])
        end_time = datetime.fromisoformat(event_data["end_time"])

        event = {
            "summary": event_data["summary"],
            "location": event_data["location"],
            "description": event_data["description"],
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Europe/Warsaw"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Europe/Warsaw"},
        }

        event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
        return event_result.get("htmlLink")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def list_google_calendar_events(calendar_id='primary'):
    try:
        service = get_google_calendar_service()

        now = datetime.utcnow().isoformat() + "Z"
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except Exception as e:
        print(f"Błąd przy pobieraniu wydarzeń: {e}")
        return []

def delete_google_calendar_event(event_id, calendar_id='primary'):
    try:
        service = get_google_calendar_service()
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return True
    except Exception as e:
        print(f"Błąd przy usuwaniu wydarzenia: {e}")
        return False

        # List the next 10 events from now
        '''
        now = dt.datetime.utcnow().isoformat() + "Z"

        event_result = service.events().list(
            calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime"
        ).execute()
        events = event_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
        '''