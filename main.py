from load_csv import *
from make_csv import *

url_case = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
url_cured = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

case = load(url_case, 'case')
death = load(url_death, 'death')
cured = load(url_cured, 'cured')

df = pd.merge(case, death, how='left', on=['location', 'prov_state', 'country', 'lat', 'long', 'date'])
df = pd.merge(df, cured, how='left', on=['location', 'prov_state', 'country', 'lat', 'long', 'date'])

df = df.set_index('date')

df = df.replace({'Martinique':'France',
                'Reunion':'France',
                'French Guiana':'France',
                'Guadeloupe': 'France',
                'Mayotte': 'France',
                'Aruba': 'Netherlands',
                'Curacao': 'Netherlands',
                'Guernsey':'United Kingdom',
                'Jersey':'United Kingdom',
                'Guam': 'US'})

df_top_bydate = top_bydate(df)
df_top_bydate.to_csv('data/top_bydate.csv', index=False)

df_country = country(df)
df_country.to_csv('data/country.csv', index=False)

df_ratio = ratio(df)
df_ratio.to_csv('data/ratio.csv', index=False)

df_china = china(df)
df_china.to_csv('data/china.csv', index=False)

df_kor_adjusted = kor_adjusted(df)
df_kor_adjusted.to_csv('data/kor_adjusted.csv', index=False)
