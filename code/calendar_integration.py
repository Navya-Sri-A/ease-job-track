import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    # To load existing credentials if available
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, log in and authorize
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh token if expired
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
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