import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from event import *


class Agenda():
    def __init__(self, debugging=False):
        self.service = ''
        self.calendar_id = ''

    def connect(self, calendar_name):
        self.service = self.connect_to_agenda_api()
        self.calendar_id = self.get_calendar(calendar_name)

    def connect_to_agenda_api(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        return service

    def get_calendar(self, calendar_name):
        calendars = self.service.calendarList().list().execute()['items']
        for calendar in calendars:
            if calendar['summary'] == calendar_name:
                return calendar['id']
        else:
            created_calendar = self.service.calendars().insert(
                body={'summary': calendar_name}).execute()
            return created_calendar['id']

    def get_events(self, date_min, date_max):
        time_min = date_min.isoformat() + 'Z'
        time_max = date_max.isoformat() + 'Z'
        events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=time_min,
                                                   timeMax=time_max, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def insert_list_events(self, events):
        for event in events:
            self.insert_event(event)

    def delete_list_events(self, events):
        for event in events:
            self.delete_event(event)

    def delete_event(self, event):
        self.service.events().delete(calendarId=self.calendar_id, eventId=event.id).execute()

    def insert_event(self, event):
        gg_event = event.to_google_event()
        self.service.events().insert(calendarId=self.calendar_id, body=gg_event).execute()

    def __repr__(self):
        return str(self.events)


if __name__ == '__main__':
    file_name = "source/Scolarité_2018-10-18.html"
    edt = extract_edt.extract_edt(file_name)
    insert_into_agenda(edt)
