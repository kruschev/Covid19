from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json

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

for code_from, codes_to in routes.items():
    url = 'https://www.flightradar24.com/data/airports/{}/routes'.format(code_from)
    driver.get(url)
    WebDriverWait(driver, 10).until(
       EC.visibility_of_element_located((By.XPATH, "//div[@style]/div[@title]")))

    codes_to = set(codes_to)

    elements = driver.find_elements_by_xpath("//div[@title]")
    for element in elements:
        try:
            code_to = element.get_attribute('title')[-9:-6]
            if code_to in codes_to:
                print(code_from, code_to)
                add_status(code_from, code_to, 1)
                codes_to -= {code_to}
        except:
            continue

    for code_to in codes_to:
        add_status(code_from, code_to, 0)

driver.quit()

with open('flight_radar.json', 'w') as file:
    json.dump(flight_status, file)
