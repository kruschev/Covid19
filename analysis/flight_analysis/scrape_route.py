from selenium import webdriver
import json
import country_converter as coco

with open('airport.json', 'r') as file:
    airports = json.load(file)

routes = {}

driver = webdriver.Chrome()

for code, country_from in zip(airports['code'], airports['country']):
    url = 'https://www.flightsfrom.com/{}/destinations'.format(code)
    driver.get(url)

    destinations = []

    try:
        elements = driver.find_elements_by_class_name('airport-content-destination-list-name')
        for element in elements:
            text = element.get_attribute('innerText').strip().split('\n')
            country_to = coco.convert(names=text[-1].strip(), to='short_name', not_found=None)
            if country_to != country_from:
                destinations.append(text[0].split()[-1])
    except:
        print('Something is wrong')
        destinations = []

    routes[code] = destinations

driver.quit()

with open('destination.json', 'w') as file:
    json.dump(routes, file)
