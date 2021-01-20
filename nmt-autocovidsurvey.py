#!/usr/bin/python

# NMT-AutoCovidSurvey: Python script for filling out the NMT COVID-19
# survey. Copyright (C) 2021 Alexander Bethel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import sys
import toml
from selenium import webdriver
from chromedriver_py import binary_path

# URL of the Google form.
FORM_URL = ('https://docs.google.com/forms/d/e/'
            '1FAIpQLSews7FpP8CkoNBNbByDvGiqVZ1kJRd8K5FTSVhgOC60LTZJwA'
            '/viewform')

# ID of the Google form. This is a number that shows up repeatedly in
# the DOM of the pages.
FORM_ID = 'mG61Hd'

# Whether to run a headless window. This should be `True` in
# production, set it to `False` in testing to see what the browser is
# doing.
HEADLESS = True

# Whether to actually submit the form. If this is `False`, the program
# will halt one step before actually clicking the `Submit` button.
SUBMIT = True

# Amount of time to wait for Google animations (drop down menus
# expanding and closing, `Next` button proceeding between pages) to do
# their thing.
ANIM_TIME = 0.1


# Fills out the COVID-19 screening form.
def fill_out_form():
    config = load_config()
    driver = init_driver()

    setup_cookie(config, driver)
    driver.get(FORM_URL)

    print("Starting the form")
    personal_page(config, driver)
    if config['on_campus']:
        symptom_page(config, driver)
    agreement_page(config, driver)
    print("Form done")


# Fills out the personal information page (first page of the screening
# form).
def personal_page(config, driver):
    print("Filling out personal info page")

    name_element = driver.find_element_by_xpath(
        "//input[@type='text']"
    )
    phone_element = driver.find_element_by_xpath(
        "(//input[@type='text'])[2]"
    )
    dropdown_element = driver.find_element_by_xpath(
        f"//form[@id='{FORM_ID}']/div[2]/div/div[2]/div[3]/div/div/div[2]/"
        "div/div/div[2]"
    )
    name_element.send_keys(config['name'])
    phone_element.send_keys(sanitize_phone(config['phone']))
    dropdown_element.click()

    time.sleep(ANIM_TIME)

    # Selection of the dropdown element.
    selection_element = None
    if config['on_campus']:
        # "YES", on campus.
        selection_element = driver.find_element_by_xpath(
            f"//form[@id='{FORM_ID}']/div[2]/div/div[2]/div[3]/div/div/"
            "div[2]/div/div[2]/div[3]/span"
        )
    else:
        # "NO", not on campus.
        selection_element = driver.find_element_by_xpath(
            f"//form[@id='{FORM_ID}']/div[2]/div/div[2]/div[3]/div/div/"
            "div[2]/div/div[2]/div[4]/span"
        )
    selection_element.click()

    time.sleep(ANIM_TIME)

    next_button = driver.find_element_by_xpath(
        f"//form[@id='{FORM_ID}']/div[2]/div/div[3]/div/div/div/span/span"
    )
    next_button.click()
    time.sleep(ANIM_TIME)
    print("Personal info page done")


# Fills out the symptom page. Currently the only valid response to
# this is "no, I don't have symptoms".
def symptom_page(config, driver):
    print("Filling out symptom page")

    no_element = driver.find_element_by_xpath(
        "//div[@id='i10']/div[3]/div"
    )

    no_element.click()
    time.sleep(ANIM_TIME)

    next_button = driver.find_element_by_xpath(
        f"//form[@id='{FORM_ID}']/div[2]/div/div[3]/div/div/div[2]/"
        "span/span"
    )
    next_button.click()

    time.sleep(ANIM_TIME)
    print("Symptom page done")


# Fills out the agreement page (the one that confirms you know your
# rights and responsibilities).
def agreement_page(config, driver):
    print("Filling out agreement page")

    # I've always kinda wondered what happens if you answer "no" to
    # this. Maybe I'll try it sometime.
    okey_dokey_button = driver.find_element_by_xpath(
        f"//form[@id='{FORM_ID}']/div[2]/div/div[2]/div[2]/div/div/div[2]/"
        "div/div/label/div/div[2]/div/span"
    )
    okey_dokey_button.click()

    if SUBMIT:
        submit_button = driver.find_element_by_xpath(
            f"//form[@id='{FORM_ID}']/div[2]/div/div[3]/div/div/div[2]/"
            "span/span"
        )
        submit_button.click()
        print("Submitted the form")

    else:
        print("(Not actually submitting the form because SUBMIT = False)")

    print("Agreement page done")


# Loads the program configuration. Returns a dictionary of
# configuration parameters.
def load_config():
    config_file = None
    try:
        config_file = toml.load('config.toml')
    except FileNotFoundError:
        print('Missing config.toml.')
        print("Copy or rename 'config.def.toml' to 'config.toml', then")
        print('fill out each of the fields.')
        sys.exit(1)

    config_dict = {}
    config_dict['cookie'] = config_file['auth']['cookie']
    config_dict['name'] = config_file['info']['name']
    config_dict['phone'] = config_file['info']['phone']
    config_dict['symptoms'] = config_file['status']['symptoms']
    config_dict['on_campus'] = config_file['status']['on_campus']

    # Do some quick checks to make sure we support this particular
    # situation.
    if config_dict['symptoms']:
        print('''This script does not currently support reporting symptoms. \
For now,
you'll have to fill out the form manually. The URL is as follows:''')
        print('')
        print(FORM_URL)
        sys.exit(1)

    return config_dict


# Sets up a WebDriver object.
def init_driver():
    # Use Google Chrome for now. TODO: Switch to Firefox, or better
    # yet something more lightweight; having bulky closed-source
    # dependencies to a small program like this is nasty.

    # This code is taken from the backend of the Aternos-On-Discord
    # bot by Makolaos.
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument('--headless')

    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; '
                         'x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.88 Safari/537.36')
    return webdriver.Chrome(options=options, executable_path=binary_path)


# Re-formats a phone number (written in any format) into a plain digit
# string.
def sanitize_phone(phone):
    return (phone
            .replace('(', '')
            .replace(')', '')
            .replace(' ', '')
            .replace('-', ''))


# Sets up the WebDriver cookie for `docs.google.com`.
def setup_cookie(config, driver):
    # The officially recommended Selenium way of doing this is to
    # navigate to the 404 page, then write the cookies, then visit the
    # page you actually want to test. Seems kinda clunky to me, but oh
    # well -- it works, and that's what really matters.
    driver.get('https://docs.google.com/invalid')
    cookie = parse_cookie(config['cookie'])

    for key in cookie:
        driver.add_cookie({
            'name': key,
            'value': cookie[key],
        })


# Converts a cookie string into a dictionary of key-value pairs.
# Cookies are inputted in text form as "key1=value1; key2=value2", and
# they are returned as a Python dictionary of the form { "key1":
# "value1", "key2": "value2" }.
def parse_cookie(cookie_str):
    cookie = {}
    records = cookie_str.split("; ")
    for record in records:
        entries = record.split("=", 1)
        key = entries[0]
        value = entries[1]

        cookie[key] = value

    return cookie


fill_out_form()
