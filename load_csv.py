import numpy as np
import pandas as pd

def load(url, measure_name):
    df = pd.read_csv(url)
    df = df.rename(columns={'Province/State':'prov_state', 'Country/Region':'country', 'Lat':'lat', 'Long':'long'})

    if measure_name == 'cured':
        df = df.iloc[:, :-1]
        df = correct_us(df)

        from datetime import datetime, timedelta

        cured_start_date = datetime.strptime('2020-03-22', '%Y-%m-%d')
        date_diff = (datetime.now() - cured_start_date).days

        for i in range(1, date_diff):
            date_to_fetch = cured_start_date + timedelta(days=i)
            url_cured_daily = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'.format(
                date_to_fetch.strftime('%m-%d-%Y'))
            cured_daily = load_recovered(url_cured_daily, date_to_fetch)
            df = pd.merge(df, cured_daily, how='outer', on=['prov_state', 'country'])

    df = df.set_index(['prov_state', 'country', 'lat', 'long'])
    df = df.stack()
    df = df.reset_index()

    cum = 'cum_' + measure_name
    df.columns = ['prov_state', 'country', 'lat', 'long', 'date', cum]

    if measure_name =='abcxyz':
        df.date = pd.to_datetime(df.date, format='%m/%d/%Y')
    else:
        df.date = pd.to_datetime(df.date, format='%m/%d/%y')

    df = df[df[cum] != 0]

    df['location'] = np.where(df.prov_state.isnull(), df.country, df.prov_state)

    if measure_name == 'case':
        df = error_correction(df)
    else:
        df = df.drop(['lat', 'long'], axis=1)

    new = 'new_' + measure_name
    df[new] = df.groupby('location')[cum].diff(1)
    df[new] = df[new].fillna(df[cum])

    df.loc[df.location == 'Greenland', 'country'] = 'Greenland'
    df.loc[df.location == 'Diamond Princess', 'country'] = 'Diamond Princess'

    return df


def load_recovered(url, date_to_fetch):
    df = pd.read_csv(url)

    df = df[['Province_State', 'Country_Region', 'Recovered']]
    df.columns = ['prov_state', 'country', date_to_fetch.strftime('%#m/%#d/%y')]

    df = correct_us(df)

    return df


def correct_us(df):
    df_non_us = df[df['country'] != 'US']
    df_us = df[df['country'] == 'US'].groupby('country', as_index=False).sum()

    df_us['prov_state'] = np.nan

    cols = list(df_us.columns)
    cols = [cols[-1]] + cols[:-1]
    df_us = df_us[cols]

    df = pd.concat([df_non_us, df_us])

    return df


# The data on March 12th for some countries were not updated correctly in the dataset. I used the data from WHO to fill in the errors
def error_correction(df):
    df.loc[(df.location == 'Japan') & (df.date == '2020-03-12'), 'cum_case'] = 675
    df.loc[(df.location == 'Italy') & (df.date == '2020-03-12'), 'cum_case'] = 15113
    df.loc[(df.location == 'Spain') & (df.date == '2020-03-12'), 'cum_case'] = 2965
    df.loc[(df.location == 'Switzerland') & (df.date == '2020-03-12'), 'cum_case'] = 858
    df.loc[(df.location == 'Netherlands') & (df.date == '2020-03-12'), 'cum_case'] = 614
    df.loc[(df.location == 'France') & (df.date == '2020-03-12'), 'cum_case'] = 2860

    return df
