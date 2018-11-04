import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import json
import credentials_window
from event import *


class EDT():

    def __init__(self, debugging=False):
        self.driver = ''
        self.username = ''
        self.password = ''
        self.schedule = []
        self._wait = ui.WebDriverWait(self.driver, 10)
        self._debugging = debugging

    def access_edt(self):
        print('Starting Google Chrome')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(chrome_options=options)
        website = 'https://scolarite.ec-lyon.fr/'
        self.driver.get(website)
        print('\nAccessing website: ' + website + ' ...')
        if self.driver.title == 'Connexion - SSO - École Centrale de Lyon':
            self.connection()
        if self.driver.title != 'Scolarité':
            self.vpn_wrong()
        self.access_edt_tab()

    def get_credentials(self):
        credentials_window.Credentials(self)

    def pass_credentials(self, a, b):
        self.username = a
        self.password = b
        self.connect()

    def connect(self):
        id = self.driver.find_element_by_id('username')
        id.clear()
        id.send_keys(self.username)
        pwd = self.driver.find_element_by_id('password')
        pwd.clear()
        pwd.send_keys(self.password)
        pwd.submit()
        if self.driver.title == 'Connexion - SSO - École Centrale de Lyon':
            self.wrong_password()

    def wrong_password(self):
        print('\nOups... Something went wrong')
        print('Please check your credentials')
        self.get_credentials()

    def connection(self):
        if self.driver.title == 'Connexion - SSO - École Centrale de Lyon':
            print('\nConnecting...')
            self.get_credentials()

    def vpn_wrong(self):
        print('\nOups... Something went wrong')
        print('Make sure you are connected to Centrale\'s VPN')
        self.driver.quit()
        exit()

    def access_edt_tab(self):
        print('\nAccessing EDT tab...')
        edt_tab = self.driver.find_element_by_name('lien_3')
        edt_tab.click()
        time.sleep(2)
        self._wait.until(self.edt_loading)
        time.sleep(0.1)

    def get_current_week(self):
        weeks = self.driver.find_element_by_id("numsemaine")
        current_week = weeks.find_element_by_xpath("//option[@selected]")
        return current_week.get_attribute("value")

    def get_max_value(self):
        weeks = self.driver.find_element_by_id("numsemaine")
        options = weeks.find_elements_by_tag_name("option")
        return options[-1].get_attribute("value")

    def get_edt_week(self, id):
        print('\nGetting week #' + str(id) + ' ...')
        weeks = self.driver.find_element_by_id("numsemaine")
        week_to_select = weeks.find_element_by_xpath(
            "//option[@value=" + str(id) + "]")
        # date format at the beginning '0 (27/08/2018) '
        #             at the end '2018-08-27'
        date = week_to_select.text.split(' ')[1]
        date = date[1:-1].split('/')
        date.reverse()
        date = '-'.join(date)
        week_to_select.click()
        print('Starting on ' + date)
        return date

    def save_source(self, file_name):
        print('\nSaving page source as ' + file_name + ' ...')
        content_page = self.driver.page_source
        with open(file_name, 'w') as f:
            f.write(content_page)

    def extract_edt(self):
        current_week_id = int(self.get_current_week())
        max_id = int(self.get_max_value())
        if self._debugging:
            max_id = current_week_id + 5  # we don't need to look at all the schedules
        for id in range(current_week_id, max_id + 1):
            first_date = self.get_edt_week(id)
            self._wait.until(self.edt_loading)
            self.extract_week_edt()
        self.driver.quit()

    def edt_loading(self, driver):
        element = self.driver.find_element_by_id('progress_abs')
        style = element.get_attribute('style')
        return 'display: none;' in style

    def extract_week_edt(self):
        rows_edt = self.driver.find_elements_by_css_selector(
            '.InfoCentreListeEDT')
        week_events = []
        for row_edt in rows_edt:
            event = Event(row_edt)
            event.extract_event()
            event.format_event()
            if event.title != '':
                week_events.append(event)
        if len(week_events) > 0:
            self.group_events(week_events)

    def group_events(self, week_events):
        i = 0
        event = week_events[i]
        while i < len(week_events) - 1:
            next_event = week_events[i + 1]
            if event.title == next_event.title and \
                    event.location == next_event.location:
                event.merge_events(next_event)
            else:
                self.schedule.append(event)
                event = week_events[i + 1]
            i += 1
        if len(week_events) > 0 and i < len(week_events):
            self.schedule.append(event)

        def list_per_day(self):
            # create a list of events per day
            self.events_per_day = {}
            for event in self.schedule:
                key = event.start_datetime.strftime('%Y-%m-%d')
                if key not in self.events_per_day.keys():
                    self.events_per_day[key] = []
                self.events_per_day[key].append(event)

    def create_json(self):
        output = []
        for event in self.schedule:
            output.append(event.to_dict())
        return output

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def save(self, file_name):
        content = self.create_json()
        with open(file_name, 'w') as f:
            json.dump(content, f, default=self.json_serial, indent="\t")

    def open(self, file_name):
        print('Loading ' + file_name + ' ...')
        with open(file_name, 'r') as f:
            content = json.load(f)
        for event in content:
            evt = Event()
            evt.from_dict(event)
            self.schedule.append(evt)
        print('... ' + file_name + ' loaded')

    def create_from_google(self, events):
        for event in events:
            evt = Event()
            evt.from_google_event(event)
            self.schedule.append(evt)

    def compare_edt(self, edt):
        new = []
        for event in self.schedule:
            if event not in edt.schedule:
                new.append(event)
        old = []
        for event in edt.schedule:
            if event not in self.schedule:
                old.append(event)
        return new, old

    def __repr__(self):
        return str(self.schedule)


if __name__ == '__main__':
    edt = EDT()
    # print(len(edt))
