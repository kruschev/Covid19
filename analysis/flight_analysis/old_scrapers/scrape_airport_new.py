from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
import country_converter as coco


driver = webdriver.Chrome()

parent_url = 'https://airports-list.com/airports'

driver.get(parent_url)

urls = []
countries = driver.find_elements_by_xpath("//span[@class='field-content']/a")
for country in countries:
    name = country.text
    link = country.get_attribute('href')
    urls.append((name, link))

data = {'country':[],
        'city': [],
        'name': [],
        'code': []
        }

for url in urls:
    country_name = url[0]

    driver.get(url[1])
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "views-row-last")))

    info = driver.find_element_by_id("datatable-1_info").text.split(' ')
    loaded_rows = int(info[-4].replace(',', ''))
    total_rows = int(info[-2].replace(',', ''))

    while loaded_rows <= total_rows:
        cities = driver.find_elements_by_class_name("views-field-field-gorod-eng")[1:]
        airport_names = driver.find_elements_by_class_name("views-field-field-name-eng")[1:]
        airport_codes = driver.find_elements_by_class_name("views-field-title-3")[1:]
        icaos = driver.find_elements_by_class_name("views-field-field-icao")[1:]

        for city, airport_name, airport_code, icao in zip(cities, airport_names, airport_codes, icaos):
            if icao.text != '':
                data['country'].append(country_name)
                data['city'].append(city.text)
                data['name'].append(airport_name.text)
                data['code'].append(airport_code.text)

        if loaded_rows == total_rows:
            break
        next_btn = driver.find_element_by_id("datatable-1_next")
        next_btn.click()
        loaded_rows = int(driver.find_element_by_id("datatable-1_info").text.split(' ')[-4].replace(',', ''))

    if country_name == 'Zimbabwe':
        break

data['country'] = coco.convert(names=data['country'], to='short_name', not_found=None)

driver.quit()

with open('airport.json', 'w') as file:
    json.dump(data, file)