import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz 

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    # Load existing credentials if available
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)  # Fix: Load credentials first
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Fix: Refresh only if creds are valid

    # If no valid credentials, log in and authorize
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)

def add_interview_to_calendar(company_name, job_title, interview_date):  #It adds the Interview date to the google calendar
    service = get_calendar_service()

    PACIFIC_TIMEZONE = "America/Los_Angeles"  # Setting Pacific Time Zone
    tz = pytz.timezone(PACIFIC_TIMEZONE)

    # Convert interview_date to ISO format
    interview_start = datetime.strptime(interview_date, "%Y-%m-%dT%H:%M")
    interview_end = interview_start + timedelta(hours=1)  # 1-hour interview

    interview_start_pacific = tz.localize(interview_start)
    interview_end_pacific = tz.localize(interview_end)
    event = {
        "summary": f"Interview: {job_title} at {company_name}",
        "start": {
            "dateTime": interview_start_pacific.astimezone(pytz.utc).isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": interview_end_pacific.astimezone(pytz.utc).isoformat(),
            "timeZone": "UTC",
        },
    }

    try:
        event_result = service.events().insert(calendarId="primary", body=event).execute()
        event_id = event_result.get("id")

        print(f"Event created: {event_result.get('htmlLink')}")
        return event_id 
    except Exception as e:
        print("Error creating event:", e)
        return None
    

def add_reminder_to_calendar(company_name, job_title, reminder_date): # Adds Reminder to the Google calendar
    service = get_calendar_service()

    PACIFIC_TIMEZONE = "America/Los_Angeles"  # Setting Pacific Time Zone
    tz = pytz.timezone(PACIFIC_TIMEZONE)

    try:
        reminder_start = datetime.strptime(reminder_date, "%Y-%m-%dT%H:%M")
    except ValueError:
        reminder_start = datetime.strptime(reminder_date, "%Y-%m-%d")
        reminder_start = reminder_start.replace(hour=9, minute=0)

    reminder_end = reminder_start + timedelta(hours=1)

    # Convert to Pacific Time and then to UTC for Google Calendar
    reminder_start_pacific = tz.localize(reminder_start)
    reminder_end_pacific = tz.localize(reminder_end)


    event = {
        "summary": f"Reminder: Follow-up for {job_title} at {company_name}",
        "start": {
            "dateTime": reminder_start_pacific.astimezone(pytz.utc).isoformat(), # UTC for Google
            "timeZone": "UTC", 
        },
        "end": {
            "dateTime": reminder_end_pacific.astimezone(pytz.utc).isoformat(), # UTC for Google
            "timeZone": "UTC", 
        },
    }

    try:
        event_result = service.events().insert(calendarId="primary", body=event).execute()
        event_id = event_result.get("id")
        print(f"Reminder created: {event_result.get('htmlLink')}")
        
        return event_id 
    except Exception as e:
        print("Error creating reminder event:", e)
        return None

def delete_event_from_calendar(event_id): # When a particular job is deleted from the list it deletes the event from the calendar
    service = get_calendar_service()
    try:
        if event_id: 
            service.events().delete(calendarId="primary", eventId=event_id).execute()
            print(f"Deleted event {event_id} from Google Calendar")
        else:
            print("No event ID provided for deletion.")
    except Exception as e:
        print("Error deleting event:", e)
