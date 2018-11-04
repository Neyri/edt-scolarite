from datetime import datetime


class Event():
    def __init__(self, source=''):
        self._source = source
        self.title = ''
        self.start_datetime = datetime.now()
        self.end_datetime = datetime.now()
        self.location = ''
        self._data = {}
        self.id = ''

    def from_google_event(self, gg_event):
        self.id = gg_event['id']
        self.title = gg_event['summary']
        if 'location' in gg_event.keys():
            self.location = gg_event['location']
        start = gg_event['start']['dateTime'].split('+')[0]
        self.start_datetime = self.create_datetime(date_time=start)
        end = gg_event['end']['dateTime'].split('+')[0]
        self.end_datetime = self.create_datetime(date_time=end)

    def to_google_event(self):
        event = {
            'summary': self.title,
            'location': self.location,
            'start': {
                'dateTime': self.start_datetime.isoformat(),
                'timeZone': 'Europe/Paris'
            },
            'end': {
                'dateTime': self.end_datetime.isoformat(),
                'timeZone': 'Europe/Paris'
            }
        }
        if self.id != '':
            event['id'] = self.id
        return event

    def extract_event(self):
        cols = self._source.find_elements_by_tag_name('td')
        name = self.extract_unique_name(cols[6].text)
        self._data = {
            'date': cols[1].text,
            'hour': cols[2].text,
            'type': cols[3].text,
            'name': name,
            'room': cols[8].text
        }

    def format_event(self):
        if self._data['room'] != '' or self._data['type'] != 'Autonomie':
            self.title = self.create_title()
            date = self._data['date'].split(' ')[1]
            hour = self._data['hour']
            [start_hour, end_hour] = hour.split('-')
            self.start_datetime = self.create_datetime(
                date=date, time=start_hour)
            self.end_datetime = self.create_datetime(date=date, time=end_hour)
            self.location = self._data['room']

    def merge_events(self, next_event):
        self.end_datetime = next_event.end_datetime

    def extract_unique_name(self, text):
        # format 'MR MOD 2.1 - Défis informatiques du Big DataMR MOD 2.1 - Défis informatiques du Big DataMR MOD 2.1 - Défis informatiques du Big DataMOD 2.1 - Défis informatiques du Big Data'
        # some info are repeated
        splitter = text.split(' - ')[0]
        name = text.split(splitter + ' - ')[1]
        return name

    def create_datetime(self, date='', time='', date_time=''):
        if date != '' and time != '':
            datetime_format = '%d/%m/%Y %H:%M'
            return datetime.strptime(
                date + ' ' + time, datetime_format)
        if date_time != '':
            datetime_format = '%Y-%m-%dT%H:%M:%S'
            return datetime.strptime(
                date_time, datetime_format)

    def create_title(self):
        lesson_type = self._data['type']
        name = self._data['name']
        if lesson_type.isalpha():
            if self.is_a_vowel(name):
                title = lesson_type + ' d\'' + name
            else:
                title = lesson_type + ' de ' + name
        else:
            title = name
        return title

    def is_a_vowel(self, text):
        vowels_list = ['a', 'e', 'i', 'o', 'u', 'y']
        first_letter = text[0].lower()
        return first_letter in vowels_list

    def to_dict(self):
        dict = {
            'title': self.title,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime
        }
        if self.location != '':
            dict['location'] = self.location
        if self.id != '':
            dict['id'] = self.id
        return dict

    def from_dict(self, dict):
        isoformat = '%Y-%m-%dT%H:%M:%S'
        self.title = dict['title']
        self.start_datetime = datetime.strptime(
            dict['start_datetime'], isoformat)
        self.end_datetime = datetime.strptime(
            dict['end_datetime'], isoformat)
        self.location = dict['location'] if 'location' in dict.keys() else ''
        self.id = dict['id'] if 'id' in dict.keys() else ''

    def __eq__(self, other):
        return self.title == other.title and \
            self.start_datetime == other.start_datetime and \
            self.end_datetime == other.end_datetime and \
            self.location == other.location

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return self.title + ' from ' + str(self.start_datetime) + \
            ' to ' + str(self.end_datetime) + \
            (' at ' + self.location if self.location != '' else '') +\
            (' with Google id : "' + self.id + '"' if self.id != '' else '')
