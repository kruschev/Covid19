import pandas as pd

df = pd.read_csv('flight_status.csv')
# df_us = pd.read_csv('flight_status_us.csv')
# df = pd.concat([df, df_us])

airport = pd.read_json('airport_info.json')


def merge(left, right, i):
    merged = pd.merge(left, right, how='left', left_on=i, right_on='code')
    merged = merged.rename(columns={"country": "country_" + i, "city": "city_" + i, "name": "name_" + i})

    return merged.iloc[:,:-1]


df = merge(df, airport, 'from')
df = merge(df, airport, 'to')

df.to_csv('flight_status_merged.csv', index=False)