from selenium import webdriver
import json
import pandas as pd
import time

with open('flight_radar.json', 'r') as file:
    flight_status = json.load(file)

correct_active = []

start_date = '2020-04-02'

driver = webdriver.Chrome()
driver.implicitly_wait(10)

for code_from, code_to, active in zip(flight_status['from'], flight_status['to'], flight_status['active']):
    if active == 1:
        url = 'https://www.google.com/flights?lite=0#flt={}.{}.{};c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(code_from, code_to,
                                                                                                      start_date)
        driver.get(url)

        try:
            button = driver.find_element_by_class_name("gws-flights-form__date-content")
            button.click()

            time.sleep(2)

            date_range = driver.find_elements_by_xpath("//calendar-day[contains(@class, 'selected-day')]/following::calendar-day[position()<=10]")
            for date in date_range:
                date_price = date.find_element_by_class_name("gws-travel-calendar__annotation")
                if date_price.text != '':
                    correct_active.append(1)
                    print((code_from, code_to, 'active'))
                    break
                print((code_from, code_to))
            else:
                correct_active.append(0)
        except:
            raise Exception
    else:
        correct_active.append(0)

driver.quit()

flight_status['active'] = correct_active

df = pd.DataFrame(flight_status)
df.to_csv('flight_status.csv', index=False)
