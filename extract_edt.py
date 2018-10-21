from bs4 import BeautifulSoup
import datetime


def extract_unique_name(text):
    # format 'MR MOD 2.1 - Défis informatiques du Big DataMR MOD 2.1 - Défis informatiques du Big DataMR MOD 2.1 - Défis informatiques du Big DataMOD 2.1 - Défis informatiques du Big Data'
    # some info are repeated
    splitter = text.split(' - ')[0]
    name = text.split(splitter + ' - ')[1]
    return name


def extract_edt_from_html(rows):
    # for each row we want to get
    #   the date (td #2),
    #   the hour (td #3),
    #   the type (td #4),
    #   the name (td #7),
    #   the room (td #9)
    edt = []
    for row in rows:
        cols = row.find_all('td')
        name = extract_unique_name(cols[6].text)
        data = {
            'date': cols[1].text,
            'hour': cols[2].text,
            'type': cols[3].text,
            'name': name,
            'room': cols[8].text
        }
        edt.append(data)
    return edt


def is_a_vowel(text):
    vowels_list = ['a', 'e', 'i', 'o', 'u', 'y']
    first_letter = text[0].lower()
    return first_letter in vowels_list


def create_datetime(date, time):
    datetime_format = '%d/%m/%Y %H:%M'
    return datetime.datetime.strptime(
        date + ' ' + time, datetime_format)


def create_title(lesson_type, name):
    if lesson_type.isalpha():
        if is_a_vowel(name):
            title = lesson_type + ' d\'' + name
        else:
            title = lesson_type + ' de ' + name
    else:
        title = name
    return title


def format_edt(edt):
    # for each row we want
    #   title
    #   start_datetime
    #   end_datetime
    #   location
    new_edt = []
    for row in edt:
        if row['room'] != '' or row['type'] != 'Autonomie':
            title = create_title(row['type'], row['name'])
            date = row['date'].split(' ')[1]
            hour = row['hour']
            [start_hour, end_hour] = hour.split('-')
            start_datetime = create_datetime(date, start_hour)
            end_datetime = create_datetime(date, end_hour)
            location = row['room']
            data = {
                'title': title,
                'start_datetime': start_datetime.isoformat(),
                'end_datetime': end_datetime.isoformat(),
                'location': location
            }
            new_edt.append(data)
    return new_edt


def merge_rows(row1, row2):
    row1['end_datetime'] = row2['end_datetime']
    return row1


def group_events(edt):
    new_edt = []
    i = 0
    while i < len(edt) - 1:
        row = edt[i]
        next_row = edt[i + 1]
        if row['title'] == next_row['title'] and \
                row['location'] == next_row['location']:
            new_row = merge_rows(row, next_row)
            new_edt.append(new_row)
            i += 1
        else:
            new_edt.append(row)
        i += 1
    if len(edt) > 0 and i < len(edt):
        row = edt[i]
        new_edt.append(row)
    return new_edt


def extract_edt(file_name):
    with open(file_name) as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # the schedule has the id "tablecreneau" but it's not the only one... --' (it's the second one)
    edt = soup.find_all(id="tablecreneau")[1]

    rows_edt = edt.find_all("tr", {"class": "InfoCentreListeEDT"})

    edt = extract_edt_from_html(rows_edt)
    edt = format_edt(edt)
    edt = group_events(edt)
    return edt


if __name__ == '__main__':
    file_name = "source/Scolarité_2018-10-29.html"
    edt = extract_edt(file_name)
    print(edt)
