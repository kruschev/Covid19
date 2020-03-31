import pandas as pd

df = pd.read_csv('flight_status.csv')
airport = pd.read_json('airport.json')


def merge(left, right, i):
    merged = pd.merge(left, right, how='left', left_on=i, right_on='code')
    merged = merged.rename(columns={"country": "country_" + i, "location": "location_" + i, "name": "name_" + i})

    return merged.iloc[:,:-1]


df = merge(df, airport, 'from')
df = merge(df, airport, 'to')

df.to_csv('flight_status_merged.csv', index=False)