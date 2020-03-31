from selenium import webdriver
import json
import pandas as pd

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


driver = webdriver.Chrome()

for dep, arrs in routes.items():
    code_from = dep.split('_')[0]

    codes_to = {arr[0] for arr in arrs}

    url = 'https://www.flightradar24.com/data/airports/{}/routes'.format(code_from)
    driver.get(url)

    try:
        elements = driver.find_elements_by_xpath("//div[@title]")

        for element in elements:
            code_to = element.get_attribute('title')[-9:-6]
            if code_to in codes_to:
                add_status(code_from, code_to, 1)
                codes_to -= {code_to}
    except:
        raise Exception

    for code_to in codes_to:
        add_status(code_from, code_to, 0)

driver.quit()

df = pd.DataFrame(flight_status)
df.to_csv('flight_status.csv', index=False)