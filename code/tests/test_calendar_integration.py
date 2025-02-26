import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call, mock_open
from datetime import datetime

# Adding the project root directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from calendar_integration import add_interview_to_calendar, get_calendar_service, add_reminder_to_calendar

class TestAddInterviewToCalendar(unittest.TestCase):
    @patch('calendar_integration.get_calendar_service')
    def test_add_interview_to_calendar_success(self, mock_get_calendar_service):
        # Mocking the Google Calendar service
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service

        # Event insertion mocking
        mock_event_result = MagicMock()
        mock_event_result.get.side_effect = ['event_id_123', 'https://example.com/event_link']  
        mock_service.events.return_value.insert.return_value.execute.return_value = mock_event_result

        # Test data
        company_name = "Test Company"
        job_title = "Software Engineer"
        interview_date = "2023-10-15T14:00"

        event_id = add_interview_to_calendar(company_name, job_title, interview_date)

        # Assertions
        self.assertEqual(event_id, 'event_id_123')
        mock_service.events.return_value.insert.assert_called_once()

        mock_event_result.get.assert_has_calls([call('id'), call('htmlLink')])

    @patch('calendar_integration.get_calendar_service')
    def test_add_interview_to_calendar_failure(self, mock_get_calendar_service):
        # Mocking the Google Calendar service
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service

        # Raising exception - mock
        mock_service.events.return_value.insert.return_value.execute.side_effect = Exception("API Error")

        company_name = "Test Company"
        job_title = "Software Engineer"
        interview_date = "2023-10-15T14:00"

        event_id = add_interview_to_calendar(company_name, job_title, interview_date)

        # Assertions
        self.assertIsNone(event_id)
        mock_service.events.return_value.insert.assert_called_once()

class TestAddReminderToCalendar(unittest.TestCase):
    @patch('calendar_integration.get_calendar_service')
    @patch('calendar_integration.datetime')
    def test_add_reminder_to_calendar_success(self, mock_datetime, mock_get_calendar_service):
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service

        mock_event_result = MagicMock()
        mock_event_result.get.return_value = 'reminder_event_id_123'
        mock_service.events.return_value.insert.return_value.execute.return_value = mock_event_result

        # Mocking datetime 
        mock_datetime.strptime.return_value = datetime(2023, 10, 15, 9, 0)  # Naive datetime (no timezone)
        mock_datetime.timedelta.return_value = MagicMock()

        company_name = "Test Company"
        job_title = "Software Engineer"
        reminder_date = "2023-10-15T09:00"

        event_id = add_reminder_to_calendar(company_name, job_title, reminder_date)

        # Assertions
        self.assertEqual(event_id, 'reminder_event_id_123')
        mock_service.events.return_value.insert.assert_called_once()

    @patch('calendar_integration.get_calendar_service')
    @patch('calendar_integration.datetime')
    def test_add_reminder_to_calendar_failure(self, mock_datetime, mock_get_calendar_service):
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service

        mock_service.events.return_value.insert.return_value.execute.side_effect = Exception("API Error")

        mock_datetime.strptime.return_value = datetime(2023, 10, 15, 9, 0)  # Naive datetime (no timezone)
        mock_datetime.timedelta.return_value = MagicMock()

        company_name = "Test Company"
        job_title = "Software Engineer"
        reminder_date = "2023-10-15T09:00"

        event_id = add_reminder_to_calendar(company_name, job_title, reminder_date)

        # Assertions
        self.assertIsNone(event_id)
        mock_service.events.return_value.insert.assert_called_once()

if __name__ == '__main__':
    unittest.main()

    