import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_calendar_service(user_email):
    if not user_email:
        print("Adres e-mail nie został podany.")
        return None

    creds = None
    token_file = f"token_{user_email}.json"

    # Sprawdź, czy token istnieje
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)

    # Odśwież token lub uzyskaj nowy
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Zapisz token dla danego użytkownika
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    if creds:
        return build("calendar", "v3", credentials=creds)
    else:
        print(f"Nie można utworzyć usługi Google Calendar dla użytkownika {user_email}.")
        return None

def create_google_calendar_event(event_data,user_email ,calendar_id="primary"):
    try:
        service = get_google_calendar_service(user_email)

        if not service:
            print("Nie udało się uzyskać dostępu do usługi Google Calendar.")
            return None

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

def list_google_calendar_events(user_email, calendar_id='primary'):
    try:
        service = get_google_calendar_service(user_email)

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

def delete_google_calendar_event(event_id,user_email ,calendar_id='primary'):
    try:
        service = get_google_calendar_service(user_email)
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