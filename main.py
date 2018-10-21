import get_scolarite_edt
import insert_agenda
import os
import datetime
import extract_edt
from httplib2 import Http
from oauth2client import file, client, tools


def get_current_monday():
    today = datetime.date.today()
    today = today.isocalendar()
    year = str(today[0])
    week_nb = str(today[1] - 1)
    day = '1'
    monday = ', '.join([year, week_nb, day])
    format = '%Y, %U, %w'
    monday = datetime.datetime.strptime(monday, format)
    return monday.strftime('%Y-%m-%d')


def get_monday_from_filename(file_name):
    return file_name.split('_')[1].split('.')[0]


def main():
    if 'source' not in os.listdir():
        os.mkdir('source')
    # get_scolarite_edt.main()
    dir = 'source/'
    sources = os.listdir(dir)
    current_monday = get_current_monday()
    current_week_file = 'Scolarité_' + current_monday + '.html'
    service = insert_agenda.connect_to_agenda_api()
    calendar_id = insert_agenda.get_calendar_edt(service)
    connectors = [service, calendar_id]
    for source in sources:
        if source >= current_week_file:
            monday = get_monday_from_filename(source)
            print("\nWeek starting on", monday)
            edt = extract_edt.extract_edt(dir + source)
            insert_agenda.insert_into_agenda(edt, monday, connectors)


if __name__ == '__main__':
    main()
