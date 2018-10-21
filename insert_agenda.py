import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import extract_edt


def connect_to_agenda_api():
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service


def get_calendar_edt(service):
    calendars = service.calendarList().list().execute()['items']
    for calendar in calendars:
        if calendar['summary'] == 'EDT Centrale Lyon':
            return calendar['id']
    else:
        calendar = {
            'summary': 'EDT Centrale Lyon'
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        return created_calendar['id']


def format_edt_into_event(edt):
    event = {
        'summary': edt['title'],
        'location': edt['location'],
        'start': {
            'dateTime': edt['start_datetime'],
            'timeZone': 'Europe/Paris'
        },
        'end': {
            'dateTime': edt['end_datetime'],
            'timeZone': 'Europe/Paris'
        }
    }
    return event


def get_events_week(week, connectors=[]):
    service, calendar_id = connectors
    time_min = datetime.datetime.strptime(week, '%Y-%m-%d')
    time_max = time_min + datetime.timedelta(days=6)
    time_min = time_min.isoformat() + 'Z'
    time_max = time_max.isoformat() + 'Z'
    events_result = service.events().list(calendarId=calendar_id, timeMin=time_min,
                                          timeMax=time_max, singleEvents=True,
                                          orderBy='startTime').execute()
    week_events = events_result.get('items', [])
    return week_events


def is_already_in_calendar(event, week_events):
    for week_event in week_events:
        week_event_start = week_event['start']['dateTime'].split('+')[0]
        if week_event_start == event['start']['dateTime']:
            return True, week_event
    return False, None


def has_to_be_updated(week_event, event):
    # the week event has to be updated if
    # the summary is different or the location is different
    if 'location' in week_event.keys():
        return week_event['location'] != event['location'] or \
            week_event['summary'] != event['summary']
    else:
        return week_event['summary'] != event['summary']


def update_event(week_event, event):
    new_event = {
        'start': week_event['start'],
        'end': week_event['end']
    }
    if week_event['location'] != event['location']:
        new_event['location'] = event['location']
    if week_event['summary'] != event['summary']:
        new_event['summary'] = event['summary']
    return new_event


def insert_into_agenda(edt, week, connectors=[]):
    service, calendar_id = connectors
    week_events = get_events_week(week, connectors=connectors)
    inserted = 0
    updated = 0
    for lesson in edt:
        event = format_edt_into_event(lesson)
        in_calendar, week_event = is_already_in_calendar(event, week_events)
        if not in_calendar:
            service.events().insert(calendarId=calendar_id, body=event).execute()
            inserted += 1
        else:
            if has_to_be_updated(week_event, event):
                new_event = update_event(week_event, event)
                updated += 1
                service.events().update(calendarId=calendar_id,
                                        eventId=week_event['id'], body=new_event).execute()
    print(str(inserted) + " events inserted"
          if inserted > 0 else "Nothing was inserted")
    print(str(updated) + " events updated"
          if updated > 0 else "Nothing was updated")


if __name__ == '__main__':
    file_name = "source/Scolarité_2018-10-18.html"
    edt = extract_edt.extract_edt(file_name)
    insert_into_agenda(edt)
