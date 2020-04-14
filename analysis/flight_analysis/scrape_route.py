from selenium import webdriver
import json
import country_converter as coco

with open('airport.json', 'r') as file:
    airports = json.load(file)

routes = {}

codes_from = set(airports['code'])
scraped = set()
left_over = []

airports_info = {'country':[],
                'city': [],
                'code': []
                }

driver = webdriver.Chrome()

for code_from, country_from in zip(airports['code'], airports['country']):
    url = 'https://www.flightsfrom.com/{}/destinations'.format(code_from)
    driver.get(url)

    destinations = []

    try:
        elements = driver.find_elements_by_class_name('airport-content-destination-list-name')
        for element in elements:
            text = element.get_attribute('innerText').strip().split('\n')
            country_to = coco.convert(names=text[-1].strip(), to='short_name', not_found=None)
            if country_to != country_from:
                code_to = text[0].split()[-1]
                destinations.append(code_to)
                if code_to not in scraped:
                    scraped.add(code_to)
                    airports_info['country'].append(country_to)
                    airports_info['city'].append(text[0].rsplit(' ', 1)[0])
                    airports_info['code'].append(code_to)
                if code_to not in codes_from:
                    left_over.append((code_to, country_to))

    except:
        print('Something is wrong')
        destinations = []

    routes[code_from] = destinations

for item in left_over:
    url = 'https://www.flightsfrom.com/{}/destinations'.format(item[0])
    driver.get(url)

    destinations = []

    try:
        elements = driver.find_elements_by_class_name('airport-content-destination-list-name')
        for element in elements:
            text = element.get_attribute('innerText').strip().split('\n')
            country_to = coco.convert(names=text[-1].strip(), to='short_name', not_found=None)
            if country_to != item[1]:
                code_to = text[0].split()[-1]
                destinations.append(code_to)
                if code_to not in scraped:
                    scraped.add(code_to)
                    airports_info['country'].append(country_to)
                    airports_info['city'].append(text[0].rsplit(' ', 1)[0])
                    airports_info['code'].append(code_to)
    except:
        print('Something is wrong')
        destinations = []

    routes[item[0]] = destinations

driver.quit()

with open('destination.json', 'w') as file:
    json.dump(routes, file)

with open('airport_info.json', 'w') as file:
    json.dump(airports_info, file)