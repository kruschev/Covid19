from selenium import webdriver
import json
import pandas as pd


driver = webdriver.Chrome()

url = 'https://www.google.com/flights?lite=0#flt=CDG.IST.2020-04-01;c:USD;e:1;s:0;sd:1;t:f;tt:o'
driver.get(url)

try:
    button = driver.find_element_by_class_name("gws-flights-form__date-content")
    button.click()

    element = driver.find_element_by_class_name("v3QEjzHx7cS__edge-effects")
    print(element)
except:
    raise Exception