from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from collections import defaultdict
import time

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

with open('destination.json', 'r') as file:
    routes = json.load(file)

options = webdriver.ChromeOptions()
options.add_argument('--lang=en')
driver = webdriver.Chrome(options=options)

codes = set()
city_dict = defaultdict(list)

for _, codes_to in routes.items():
    for code_to in codes_to:
        if code_to not in codes:
            url = 'https://www.google.com/flights?hl=en#flt={}.BIN.;c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(code_to)
            driver.get(url)

            WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).\
                until(EC.presence_of_element_located((By.CLASS_NAME, "gws-flights-form__location-list")))

            city_name = driver.find_element_by_class_name("gws-flights-form__location-list").text[:-3]
            while city_name == code_to:
                try:
                    city_name = driver.find_element_by_class_name("gws-flights-form__location-list").text[:-3]
                except:
                    time.sleep(2)

            city_dict[city_name].append(code_to)
            codes.add(code_to)

driver.quit()

with open('city_name.json', 'w') as file:
    json.dump(city_dict, file)
