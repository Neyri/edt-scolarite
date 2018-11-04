from edt import *
from agenda import *
import os
import datetime
from httplib2 import Http
from oauth2client import file, client, tools
from check_window import *


def get_current_monday():
    today = datetime.date.today()
    today = today.isocalendar()
    year = str(today[0])
    week_nb = str(today[1] - 1)
    day = '1'
    monday = ', '.join([year, week_nb, day])
    format = '%Y, %U, %w'
    monday = datetime.datetime.strptime(monday, format)
    return monday


def main():
    """
        x extract all events from scolarité
        x build a calendar with all the events upcoming
        x get all the upcoming events
        - format upcoming events
        - create a list of actions to do
            insert
            update
            delete
        - ask the user if he agrees
        - do the actions
    """
    edt_file = 'edt.json'
    edt_gg_file = 'edt_gg.json'
    edt = EDT()
    # edt.access_edt()
    # edt.extract_edt()
    # edt.save(edt_file)
    edt.open(edt_file)

    last_event = edt.schedule[-1]
    last_event_datetime = last_event.end_datetime
    current_monday = get_current_monday()

    agenda = Agenda()
    # agenda.connect('EDT Centrale Lyon')
    # events = agenda.get_events(current_monday, last_event_datetime)
    edt_gg = EDT()
    # edt_gg.create_from_google(events)
    # edt_gg.save(edt_gg_file)
    edt_gg.open(edt_gg_file)
    to_insert, to_delete = edt.compare_edt(edt_gg)

    print('%d event(s) to insert' % (len(to_insert))
          if len(to_insert) > 0 else 'No events to insert')
    print('%d event(s) to delete' % (len(to_delete))
          if len(to_delete) > 0 else 'No events to delete')
    User_check(to_insert, to_delete, agenda)


if __name__ == '__main__':
    main()
