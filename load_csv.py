import numpy as np
import pandas as pd

def load(url, measure_name):
    df = pd.read_csv(url, index_col=[0, 1, 2, 3])
    df = df.stack()
    df = df.reset_index()

    cum = 'cum_' + measure_name
    df.columns = ['prov_state', 'country', 'lat', 'long', 'date', cum]

    df.date = pd.to_datetime(df.date, format='%m/%d/%y')

    df = df[df[cum] != 0]

    df['location'] = np.where(df.prov_state.isnull(), df.country, df.prov_state)

    if measure_name == 'case':
        df = error_correction(df)

    new = 'new_' + measure_name
    df[new] = df.groupby('location')[cum].diff(1)
    df[new] = df[new].fillna(df[cum])

    return df[['location', 'prov_state', 'country', 'lat', 'long', 'date', cum, new]]  # rearrange the columns and return the df

# The data on March 12th for some countries were not updated correctly in the dataset. I used the data from WHO to fill in the errors
def error_correction(df):
    df.loc[(df.location == 'Japan') & (df.date == '2020-03-12'), 'cum_case'] = 675
    df.loc[(df.location == 'Italy') & (df.date == '2020-03-12'), 'cum_case'] = 15113
    df.loc[(df.location == 'Spain') & (df.date == '2020-03-12'), 'cum_case'] = 2965
    df.loc[(df.location == 'Switzerland') & (df.date == '2020-03-12'), 'cum_case'] = 858
    df.loc[(df.location == 'Netherlands') & (df.date == '2020-03-12'), 'cum_case'] = 614
    df.loc[(df.location == 'France') & (df.date == '2020-03-12'), 'cum_case'] = 2860

    return df
