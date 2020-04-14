from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
import pandas as pd
import time
import datetime


with open('destination.json', 'r') as file:
    routes = json.load(file)

with open('city_name.json', 'r') as file:
    cities = json.load(file)

flight_status = {"from": [],
                 "to": [],
                 "active": [],
                 "date": []
                 }


def add_status(code_from, code_to, active, date):
    flight_status["from"].append(code_from)
    flight_status["to"].append(code_to)
    flight_status["active"].append(active)
    flight_status["date"].append(date)

    return


def route_check(code_from, code_to, date):
    url = 'https://www.google.com/flights?hl=en#flt={}.{}.{};c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(code_from,
                                                                                                  code_to,
                                                                                                  date)
    try:
        driver.get(url)

        button = driver.find_element_by_class_name("gws-flights-form__date-content")
        button.click()

        time.sleep(2)

        calendar = driver.find_elements_by_xpath(
            "//calendar-day[contains(@class, 'selected-day')]/following::calendar-day[position()<=14]")
        for d in calendar:
            price = d.find_element_by_class_name("gws-travel-calendar__annotation")
            if price.text != '':
                add_status(code_from, code_to, 1, date)
                print(f'{code_from}_{code_to}_routecheck_1')
                break
        else:
            add_status(code_from, code_to, 0, date)
            print(f'{code_from}_{code_to}_routecheck_0')

        return
    except:
        return


def explore(code_from, date):
    url = 'https://www.google.com/flights?hl=en#flt={}..{};c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(code_from, date)
    try:
        driver.get(url)

        button = driver.find_elements_by_class_name("gws-flights-form__input-container")[1]
        button.click()
        time.sleep(2)
    except:
        return []

    try:
        button = driver.find_element_by_class_name("vrfBC")
        button.click()
    except:
        print(code_from + ': no flight ' + date)
        return []

    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "VfPpkd-LgbsSe-OWXEXe-MV7yeb")))

        stops = driver.find_element_by_class_name("VfPpkd-LgbsSe-OWXEXe-MV7yeb")
        stops.click()
        no_stop = driver.find_element_by_id("i22")
        no_stop.click()

        time.sleep(2)
        zoom_btn = driver.find_elements_by_class_name("gm-control-active")[2]
        for i in range(2):
            zoom_btn.click()

        # WebDriverWait(driver, 5).until(
        #     EC.visibility_of_element_located((By.CLASS_NAME, "wIuJz")))
        time.sleep(3)

        destinations = driver.find_elements_by_xpath("//div[contains(@class, 'ZjDced')]/preceding-sibling::h3")

        return destinations
    except:
        return []


driver = webdriver.Chrome()
driver.maximize_window()

today = datetime.datetime.today()
dates = [today + datetime.timedelta(days=x) for x in range(15)]

for code_from, codes_to in routes.items():
    codes_to = set(codes_to)

    destinations_shown = []

    for idx, date in enumerate(dates):
        if len(codes_to) <= (25-idx):
            date = date.strftime("%Y-%m-%d")

            for code_to in codes_to:
                route_check(code_from, code_to, date)
            break

        elif date == today:
            continue

        else:
            date = date.strftime("%Y-%m-%d")

            destinations = explore(code_from, date)
            for destination in destinations:
                destination = destination.text
                if destination in destinations_shown:
                    continue

                try:
                    destination_airports = cities[destination]
                    for code_to in destination_airports:
                        if code_to in codes_to:
                            add_status(code_from, code_to, 1, date)
                            print(f'{code_from}_{code_to}_explore_1')
                            codes_to -= {code_to}
                except KeyError:
                    print(destination)

                destinations_shown.append(destination)

    else:
        for code_to in codes_to:
            add_status(code_from, code_to, 0, '')
            print(f'{code_from}_{code_to}_explore_0')

driver.quit()

df = pd.DataFrame(flight_status)
df.to_csv('flight_status.csv', index=False)



