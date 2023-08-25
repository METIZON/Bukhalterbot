from datetime import datetime, timedelta, timezone
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendar:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = self.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        return creds

    def list_events(self, max_results=10):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary', timeMin=now, maxResults=max_results,  # 604e61ce6f3dbd1aa39931b2a32eac66b35def9cbe7cef64f0c922587a171148@group.calendar.google.com
                singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            print('An error occurred: %s' % error)
            return []

    def create_event(self, event_data, calendarId):
        try:
            event = self.service.events().insert(calendarId=calendarId, body=event_data).execute()  # 604e61ce6f3dbd1aa39931b2a32eac66b35def9cbe7cef64f0c922587a171148@group.calendar.google.com
            return event
        except HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def list_calendar_ids(self):
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            return {calendar['summary']: calendar['id'] for calendar in calendars}
        except HttpError as error:
            print('An error occurred: %s' % error)
            return {}

    def get_free_time_slots(self, calendar_id, target_date):
        # Define start and end of the target day
        TIME_SLOT_DURATION = timedelta(minutes=30)
        start_time = datetime.datetime.combine(target_date, datetime.time(8, 0, 0))  # Start at 8 AM
        end_time = datetime.datetime.combine(target_date, datetime.time(18, 0, 0))  # End at 6 PM

        # Retrieve events for the target day
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        free_slots = []
        prev_event_end = start_time

        for event in events:
            event_start = datetime.datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            event_end = datetime.datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')

            if (event_start - prev_event_end.replace(tzinfo=event_start.tzinfo)) >= TIME_SLOT_DURATION:
                free_slots.append((prev_event_end, event_start))

            prev_event_end = event_end

        if (end_time - prev_event_end.replace(tzinfo=end_time.tzinfo)) >= TIME_SLOT_DURATION:
            free_slots.append((prev_event_end, end_time))

        return free_slots

    def save_10min_periods(self, periods):
        result = []

        for period in periods:
            start = period[0]
            end = period[1]

            current_time = start.replace(tzinfo=timezone.utc)  # Add timezone information
            while current_time.replace(tzinfo=timezone.utc) < end.replace(tzinfo=timezone.utc):
                next_time = current_time + timedelta(minutes=10)
                if next_time.replace(tzinfo=timezone.utc) > end.replace(tzinfo=timezone.utc):
                    next_time = end

                result.append([current_time, next_time])
                current_time = next_time

        return result

    def extract_hours(self, periods):
        hour_set = set()

        for period in periods:
            start_time = period[0]
            hour_set.add(start_time.hour)

        return hour_set

    def get_time_periods_by_hour(self, hour, periods):
        selected_periods = []

        for start, end in periods:
            if start.hour == hour:
                selected_periods.append([start, end])

        return selected_periods


if __name__ == '__main__':
    calendar = GoogleCalendar()

    # List upcoming events
    # events = calendar.list_events()
    # if events:
    #     print(events)
    #     print("Upcoming events:")
    #     for event in events:
    #         start = event['start'].get('dateTime', event['start'].get('date'))
    #         print(start, event['summary'])
    #         print(event)
    #         print(event['start'].get('dateTime'))
    #         print(start := datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z"), end := datetime.datetime.strptime(event['end'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z"))
    #         given_date = datetime.datetime.strptime("2023-08-23T14:30:00+02:00", "%Y-%m-%dT%H:%M:%S%z")
    #         print(bol := start <= given_date <= end)
    #         if bol:
    #             print("reserved")

    target_date = datetime.date(2023, 8, 25)  # Change this to your desired date
    # scope = datetime.datetime.strptime("16:30:00", "%H:%M:%S")
    free_slots = calendar.get_free_time_slots('primary', target_date)
    # print(free_slots)
    # free_list = []
    # for start, end in free_slots:
    #     # print(f"Free slot: {start.time()} - {end.time()}")
    #     free_list.append([start, end])
    #     # print(start.time() <= scope.time() <= end.time())

    # print(free_list)

    result_periods = calendar.save_10min_periods(free_slots)

    # Print the resulting array of 10-minute periods
    print(result_periods)
    for period in result_periods:
        print(period[0].time(), '-', period[1].time())

    hour_set = calendar.extract_hours(result_periods)

    # Print the set of unique hours
    print(hour_set)

    free_per = calendar.get_time_periods_by_hour(12, result_periods)
    print(free_per)
    for per in free_per:
        print(per[0].time(), '-', per[1].time())

    # target_date_str = "2023-08-23T17:00:00+02:00"

    # # Create a new event
    # new_event = {
    #     'summary': 'Test Event',
    #     'start': {'dateTime': '2023-08-21T10:00:00', 'timeZone': 'UTC'},
    #     'end': {'dateTime': '2023-08-21T12:00:00', 'timeZone': 'UTC'}
    # }
    # created_event = calendar.create_event(new_event)
    # if created_event:
    #     print("Event created:", created_event['summary'])

    # List calendar IDs and names
    calendar_ids = calendar.list_calendar_ids()
    print("Calendar IDs:")
    for name, calendar_id in calendar_ids.items():
        print(f"{name}: {calendar_id}")
