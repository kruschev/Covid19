from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import json
import pandas as pd
import time

with open('destination.json', 'r') as file:
    routes = json.load(file)

flight_status = {"from": [],
                 "to": [],
                 "active": []
                 }


def add_status(code_from, code_to, active):
    flight_status["from"].append(code_from)
    flight_status["to"].append(code_to)
    flight_status["active"].append(active)

    return


start_date = '2020-04-01'

driver = webdriver.Chrome()
driver.implicitly_wait(10)

for dep, arrs in routes.items():
    code_from = dep.split('_')[0]

    codes_to = {arr[0] for arr in arrs}

    for code_to in codes_to:
        url = 'https://www.google.com/flights?lite=0#flt={}.{}.{};c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(code_from, code_to,
                                                                                                      start_date)
        # url = 'https://www.google.com/flights?lite=0#flt={}.{}.{};c:USD;e:1;s:0;sd:1;t:f;tt:o'.format('CDG',
        #                                                                                               'IST',
        #                                                                                               '2020-04-11')
        # code_from = 'CDG'
        # code_to = 'IST'
        driver.get(url)

        try:
            button = driver.find_element_by_class_name("gws-flights-form__date-content")
            button.click()

            time.sleep(2)
            #WebDriverWait(driver, 2).until(
            #    EC.invisibility_of_element_located((By.CLASS_NAME, "gws-travel-calendar__loading")))

            date_range = driver.find_elements_by_xpath("//calendar-day[contains(@class, 'selected-day')]/following::calendar-day[position()<=7]")
            for date in date_range:
                date_price = date.find_element_by_class_name("gws-travel-calendar__annotation")
                if date_price.text != '':
                    add_status(code_from, code_to, 1)
                    #print((code_from, code_to, 'active'))
                    break
                #print((code_from, code_to))
            else:
                add_status(code_from, code_to, 0)
        except:
            raise Exception

driver.quit()

df = pd.DataFrame(flight_status)
df.to_csv('flight_status.csv', index=False)
