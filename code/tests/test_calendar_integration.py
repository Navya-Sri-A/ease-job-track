import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calendar_integration import add_interview_to_calendar, delete_event_from_calendar, get_calendar_service

class TestGetCalendarService(unittest.TestCase):
    @patch('calendar_integration.pickle.load')
    @patch('calendar_integration.os.path.exists', return_value=True)
    @patch('calendar_integration.build')
    def test_get_calendar_service_with_existing_credentials(self, mock_build, mock_exists, mock_pickle_load):
        # Mock credentials
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds.expired = False
        mock_pickle_load.return_value = mock_creds
        # Call the function
        service = get_calendar_service()
        # Assertions
        self.assertIsNotNone(service)
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_creds)
    @patch('calendar_integration.pickle.dump')
    @patch('calendar_integration.pickle.load')
    @patch('calendar_integration.os.path.exists', return_value=True)
    @patch('calendar_integration.InstalledAppFlow.from_client_secrets_file')
    @patch('calendar_integration.build')
    def test_get_calendar_service_with_expired_credentials(self, mock_build, mock_flow, mock_exists, mock_pickle_load, mock_pickle_dump):
        # Mock expired credentials
        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = True
        mock_pickle_load.return_value = mock_creds
        # Mock the OAuth flow
        mock_new_creds = MagicMock()
        mock_flow.return_value.run_local_server.return_value = mock_new_creds
        # Call the function
        service = get_calendar_service()
        # Assertions
        self.assertIsNotNone(service)
        mock_creds.refresh.assert_called_once()
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_new_creds)
    @patch('calendar_integration.pickle.dump')
    @patch('calendar_integration.os.path.exists', return_value=False)
    @patch('calendar_integration.InstalledAppFlow.from_client_secrets_file')
    @patch('calendar_integration.build')
    def test_get_calendar_service_with_no_existing_credentials(self, mock_build, mock_flow, mock_exists, mock_pickle_dump):
        # Mock the OAuth flow
        mock_new_creds = MagicMock()
        mock_flow.return_value.run_local_server.return_value = mock_new_creds
        # Call the function
        service = get_calendar_service()
        # Assertions
        self.assertIsNotNone(service)
        mock_flow.assert_called_once_with("credentials.json", ["https://www.googleapis.com/auth/calendar"])
        mock_build.assert_called_once_with("calendar", "v3", credentials=mock_new_creds)
    @patch('calendar_integration.get_calendar_service')
    def test_delete_event_from_calendar(self, mock_get_service):
        # Setup mock
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        
        # Call function
        event_id = "event123"
        delete_event_from_calendar(event_id)
        
        # Assertions
        mock_get_service.assert_called_once()
        mock_service.events().delete.assert_called_once_with(calendarId="primary", eventId=event_id)
        mock_service.events().delete().execute.assert_called_once()
    
    @patch('calendar_integration.get_calendar_service')
    def test_delete_event_from_calendar_no_event_id(self, mock_get_service):
        # Setup mock
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        
        # Call function with None event_id
        delete_event_from_calendar(None)
        
        # Assertions
        mock_get_service.assert_called_once()
        mock_service.events().delete.assert_not_called()

if __name__ == '__main__':
    unittest.main()