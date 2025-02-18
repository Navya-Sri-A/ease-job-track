import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

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

def add_interview_to_calendar(company_name, job_title, interview_date):
    service = get_calendar_service()

    # Convert interview_date to ISO format
    interview_start = datetime.strptime(interview_date, "%Y-%m-%dT%H:%M")
    interview_end = interview_start + timedelta(hours=1)  # 1-hour interview

    event = {
        "summary": f"Interview: {job_title} at {company_name}",
        "start": {
            "dateTime": interview_start.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": interview_end.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "UTC",
        },
    }

    try:
        event_result = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
        return event_result
    except Exception as e:
        print("Error creating event:", e)
        return None
    

def add_reminder_to_calendar(company_name, job_title, reminder_date):
    service = get_calendar_service()

    # Handle date format with or without time
    try:
        # If reminder_date includes time (correct format)
        reminder_start = datetime.strptime(reminder_date, "%Y-%m-%dT%H:%M")
    except ValueError:
        # If reminder_date only has date, set time to 9:00 AM
        reminder_start = datetime.strptime(reminder_date, "%Y-%m-%d")
        reminder_start = reminder_start.replace(hour=9, minute=0)  # Default time

    reminder_end = reminder_start + timedelta(hours=1)  # 1-hour reminder

    event = {
        "summary": f"Reminder: Follow-up for {job_title} at {company_name}",
        "start": {
            "dateTime": reminder_start.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": reminder_end.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "UTC",
        },
    }

    try:
        event_result = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Reminder created: {event_result.get('htmlLink')}")
        return event_result
    except Exception as e:
        print("Error creating reminder event:", e)
        return None

