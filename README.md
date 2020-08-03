# Covid19

## Introduction
In this project, I used the John Hopkin University's dataset to analyze the Covid19 pandemic. Analysis was done using Python, and for the final product, I created a Tableau dashboard to monitor the situation.

main.py is run daily and the dashboard is updated accordingly.

The interactive dashboard can be viewed at
https://kruschev.github.io/covid19/dashboard.html

## Overview
Coronavirus disease 2019 (COVID-19) is a pandemic caused by the SARS-CoV-2 virus. Originated from Wuhan, it has spread to more than 180 countries and territories. The disease is extremely contagious and has seen exponential growth in many places. As more people are infected, the country's medical resources are strained and fatal cases are becomming more common. 
[ ![](tableau/info.png) ](tableau/info.png)

## Spread of the virus
[ ![](tableau/spread.gif) ](tableau/spread.gif)

## A comparison between total cases and total deaths
[ ![](tableau/casedeath.gif) ](tableau/casedeath.gif)

## Total cases/deaths per population
[ ![](tableau/ratio.png) ](tableau/ratio.png)

## Estimating the real total cases number for different countries
An interesting debate during this pandemic is the hiding of information and lack of effort in testing people by some governments. Many speculate that the real number of infected people are much higher. Meanwhile, South Korea has been praised for its transparency level and for conducting the most tests on its citizens.

Since a country is less likely to hide death resulted from the virus, I attempted to use the country's death counts and South Korea's case fatality rate (cfr) to estimate the real number of infected population. 

In addition, I also used a dataset from DXY.cn, which contains information such as age on about 3000 patients. Since the virus has been known to attack mostly older people, I can run a simple regression model to determine the coefficient of age on fatality, and use that to adjust the cfr for each country. The country's age data was retrieved from UN publication.
[ ![](tableau/adj_cases.png) ](tableau/adj_cases.png)
After the adjustment, we can see a huge increase in many countries. However, considering that these countries were at some point overwhelmed with too many patients, it's also possible that their cfr could be much higher than average.

## Comparison of number of new cases/deaths between countries
[ ![](tableau/new_case.png) ](tableau/new_case.png)

## Ranking countries on number of new cases/deaths for each week
[ ![](tableau/new_case_weekly.png) ](tableau/new_case_weekly.png)

## Span of epidemic
A snapshot of daily case/death counts for each country. The intensity of color shows the real daily count number.
[ ![](tableau/span.png) ](tableau/span.png)

## Epidemic curve
Using color to show the epidemic curve for each country, with black color being the peak(s). We can see that some countries (Iran, US, ...) are entering a second wave.
[ ![](tableau/curve.png) ](tableau/curve.png)

## Breakdown of China provinces
This image shows the distribution of cases in China, without Hubei.
[ ![](tableau/china.png) ](tableau/china.png)

## Flight Routes Analysis
I also created another dashboard to track the status of international direct flight routes around the world. Viewers can select one country/airport and see which flight routes are still active for the next 10 days. The dashboard is located at https://kruschev.github.io/flight_status/flight.html

40 out of usual 105 countries can still fly directly to US.
[ ![](tableau/flight_to.png) ](tableau/flight_to.png)

US can still fly directly to 31 out of 106 usual countries. 
[ ![](tableau/flight_from.png) ](tableau/flight_from.png)

A map of active routes around the world.
[ ![](tableau/airport_map.png) ](tableau/airport_map.png)

A map of countries banning all international flights.
[ ![](tableau/flight_banned.png) ](tableau/flight_banned.png)

A map showing how many 'hot' countries (more than 500 COVID cases) can still fly to a certain country.
[ ![](tableau/flight_risk.png) ](tableau/flight_risk.png)
