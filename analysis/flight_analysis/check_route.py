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

#routes = {"NRT": ["FRA", "CDG", "IST", "ORD", "DFW", "AMS", "ATL", "VIE", "DXB", "LHR", "PEK", "DEN", "MAD", "PVG", "SVO", "FCO", "LAX", "BRU", "ZRH", "JFK", "CPH", "CTU", "IAH", "DUS", "CAN", "EWR", "MXP", "DOH", "XIY", "DME", "ICN", "CKG", "SZX", "BKK", "YUL", "HKG", "KMG", "SIN", "BOS", "HEL", "IAD", "WAW", "DEL", "DTW", "TLV", "SFO", "KUL", "TPE", "SEA", "HGH", "YVR", "TSN", "CSX", "BOM", "MEX", "TAO", "SYD", "XMN", "CGO", "NKG", "DMK", "MNL", "WUH", "OVB", "CAI", "HRB", "SHE", "AUH", "YYC", "CGK", "DLC", "BNE", "BLR", "FOC", "SAN", "PDX", "MEL", "SGN", "DPS", "TAS", "NGB", "AKL", "YNT", "MAA", "HAN", "HNL", "CGQ", "PER", "TSE", "CMB", "SJC", "RGN", "MFM", "CEB", "PUS", "PPT", "KTM", "KHH", "CNS", "BKI", "CRK", "DAD", "VVO", "PNH", "POM", "NAN", "BWN", "CJU", "ULN", "KHV", "REP", "RMQ", "UUS", "TAE", "KOA", "OOL", "GUM", "NOU", "SPN", "SKD"]}
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


driver = webdriver.Chrome()
driver.maximize_window()

today = datetime.datetime.today()
dates = [today + datetime.timedelta(days=x) for x in range(1,15)]

for code_from, codes_to in routes.items():
    codes_to = set(codes_to)

    destinations_shown = []

    for date in dates:
        if len(codes_to) == 0:
            break

        date = date.strftime("%Y-%m-%d")
        url = 'https://www.google.com/flights?hl=en#flt={}..{};c:USD;e:1;s:0;sd:1;t:f;tt:o'.format(code_from, date)
        driver.get(url)

        button = driver.find_elements_by_class_name("gws-flights-form__input-container")[1]
        button.click()
        time.sleep(2)

        try:
            button = driver.find_element_by_class_name("vrfBC")
            button.click()

            time.sleep(4)

            stops = driver.find_element_by_class_name("VfPpkd-LgbsSe-OWXEXe-MV7yeb")
            stops.click()
            no_stop = driver.find_element_by_id("i22")
            no_stop.click()

            time.sleep(3)
            zoom_btn = driver.find_elements_by_class_name("gm-control-active")[2]
            for i in range(3):
                zoom_btn.click()
                #time.sleep(4)

            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "wIuJz")))

            destinations = driver.find_elements_by_xpath("//div[contains(@class, 'ZjDced')]/preceding::h3")
            for destination in destinations:
                destination = destination.text
                if destination in destinations_shown:
                    continue

                try:
                    destination_airports = cities[destination]
                    for code_to in destination_airports:
                        if code_to in codes_to:
                            add_status(code_from, code_to, 1, date)
                            print(flight_status)
                            codes_to -= {code_to}
                except KeyError:
                    print(destination)

                destinations_shown.append(destination)

                # driver.get(url)
                #
                # input_city = driver.find_elements_by_class_name("flt-input")[1]
                # input_city.click()
                #
                # input_text = driver.find_element_by_tag_name("input")
                # input_text.send_keys(destination)
                #
                # results = driver.find_elements_by_class_name("gws-flights-results__airports")
                # result_codes ={}
                # for result in results:
                #     result_codes += {result.text.split('-')[1]}
                #
                # for code_to in result_codes:
                #     if code_to in codes_to:
                #         add_status(code_from, code_to, 1, date)
                #         print(flight_status)
                #         codes_to -= {code_to}
                #     else:
                #         print((code_from, code_to))

        except:
            raise Exception
            print(code_from + ': no flight ' + date)

    for code_to in codes_to:
        add_status(code_from, code_to, 0, '')

driver.quit()

df = pd.DataFrame(flight_status)
df.to_csv('flight_status.csv', index=False)



