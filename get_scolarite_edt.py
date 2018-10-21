import time
from selenium import webdriver
import getpass


def get_username():
    return input('Username: ')


def get_pwd():
    return getpass.getpass()


def connection():
    driver = webdriver.Chrome()
    website = 'https://scolarite.ec-lyon.fr/'
    driver.get(website)
    print('\nAccessing website: ' + website + ' ...')
    if driver.title == 'Connexion - SSO - École Centrale de Lyon':
        print('\nConnecting...')
        id = driver.find_element_by_id('username')
        id.send_keys(get_username())
        pwd = driver.find_element_by_id('password')
        pwd.send_keys(get_pwd())
        pwd.submit()

    if driver.title != 'Scolarité':
        print('\nOups... Something went wrong')
        print('Make sure you are connected to Centrale\'s VPN')
        driver.quit()
        exit()
        return None
    return driver


def access_edt_tab(driver):
    print('\nAccessing EDT tab...')
    edt_tab = driver.find_element_by_name('lien_3')
    edt_tab.click()
    return driver


def get_current_week(driver):
    weeks = driver.find_element_by_id("numsemaine")
    current_week = weeks.find_element_by_xpath("//option[@selected]")
    return current_week.get_attribute("value")


def get_max_value(driver):
    weeks = driver.find_element_by_id("numsemaine")
    options = weeks.find_elements_by_tag_name("option")
    return options[-1].get_attribute("value")


def get_edt_week(id, driver):
    print('\nGetting week #' + str(id) + ' ...')
    weeks = driver.find_element_by_id("numsemaine")
    week_to_select = weeks.find_element_by_xpath(
        "//option[@value=" + str(id) + "]")
    # date format at the beginning '0 (27/08/2018) '
    #             at the end '2018-08-27'
    date = week_to_select.text
    date = date.split(' ')[1]
    date = date[1:-1].split('/')
    date.reverse()
    date = '-'.join(date)
    week_to_select.click()
    print('Starting on ' + date)
    return driver, date


def save_source(file_name, driver):
    print('\nSaving page source as ' + file_name + ' ...')
    content_page = driver.page_source
    with open(file_name, 'w') as f:
        f.write(content_page)


def main():
    driver = connection()
    if not driver:
        return
    driver = access_edt_tab(driver)
    time.sleep(5)
    current_week_id = int(get_current_week(driver))
    max_id = int(get_max_value(driver))
    for id in range(current_week_id, max_id + 1):
        driver, first_date = get_edt_week(id, driver)
        time.sleep(2)
        file_name = "source/Scolarité_" + first_date + ".html"
        save_source(file_name, driver)


if __name__ == '__main__':
    main()
