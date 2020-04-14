from bs4 import BeautifulSoup
import requests
import json
import country_converter as coco


def extract_text(content, pos_loc, pos_name, pos_code):
    return (content[pos_loc].text.strip(), content[pos_name].text.strip(), content[pos_code].text.strip())


data = {'country':[],
        'city': [],
        'name': [],
        'code': []}

URL = "https://en.wikipedia.org/wiki/List_of_international_airports_by_country"

page = requests.get(URL)
soup = BeautifulSoup(page.text, 'lxml')

tables = soup.findAll('table')[1:]

for table in tables:
    country = table.find_previous('span', {'class':'mw-headline'})
    if country.text.endswith('Europe'):
        country = table.find_previous('b').text
    else:
        country = country.text
        if country in ['England and Wales', 'Scotland', 'Northern Ireland']:
            country = 'United Kingdom'
        if country in ['Easter Island']:
            country = 'Chile'

    airports = table.findAll('tr')[1:]
    rowspan = 0
    temp_loc = ''
    for airport in airports:
        content = airport.findAll('td')

        if rowspan > 0:
            _, name, code = extract_text(content, 0, 0, 1)
            city = temp_loc
            rowspan -= 1
        else:
            city, name, code = extract_text(content, 0, 1, 2)

        row = [('country', country),
               ('city', city),
               ('name', name),
               ('code', code)]

        for col, val in row:
            data[col].append(val)

        if content[0].get('rowspan'):
            rowspan = int(content[0].get('rowspan')) - 1
            temp_loc = city


data['country'] = coco.convert(names=data['country'], to='short_name', not_found=None)

with open('airport.json', 'w') as file:
    json.dump(data, file)
