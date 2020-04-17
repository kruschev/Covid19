from load_csv import *
from make_csv import *

url_case = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
#url_cured_incomplete = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv'
url_cured = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

case = load(url_case, 'case')
death = load(url_death, 'death')
cured = load(url_cured, 'cured')

df = pd.merge(case, death, how='left', on=['location', 'prov_state', 'country', 'date'])
df = pd.merge(df, cured, how='left', on=['location', 'prov_state', 'country', 'date'])

df = df.set_index('date')


'''
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
'''


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
