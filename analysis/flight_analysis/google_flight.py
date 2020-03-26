from selenium import webdriver
import json

with open('airport.json', 'r') as file:
    airports = json.load(file)

lst = []

options = webdriver.ChromeOptions()
options.add_argument('--lang=en')

for dep in airports['code'][:100:20]:
    for arr in airports['code'][200:300:20]:
        url = 'https://www.google.com/flights?lite=0#flt={}.{}.2020-03-31;c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(dep, arr)
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        try:
            flights = driver.find_element_by_css_selector('.gws-flights-results__collapsed-itinerary').text
        except:
            flights = []
            continue
        lst.append((dep, arr, flights))
        driver.close()