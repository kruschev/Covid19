import numpy as np
import pandas as pd
import country_converter as coco

def copy_flag(dest, country_list):
    import os, shutil
    import config

    path = 'tableau/flags'
    dest = config.dir + dest

    files = os.listdir(path)
    shutil.rmtree(dest, ignore_errors=True)
    os.mkdir(dest)

    for file in files:
        if file == 'Cruise Ship.png':
            src = os.path.join(path, file)
            shutil.copy(src, dest)
        country_name = coco.convert(names=file.split('.')[0], to='short_name')
        if country_name in country_list:
            src = os.path.join(path, file)
            shutil.copy(src, dest)
            if country_name == 'DR Congo':
                os.rename(os.path.join(dest, file), os.path.join(dest, 'Dr Congo.png'))
            else:
                os.rename(os.path.join(dest, file), os.path.join(dest, country_name + '.png'))

    return

def top_bydate(df):
    df_top = df.groupby([pd.Grouper(freq='W', level=0), 'country']).sum()
    df_top = df_top.reset_index()
    df_top = df_top.sort_values(['date', 'new_case'], ascending=[True, False])

    for i in range(5):
        df_top[str(i+1)] = df_top.groupby('date').country.transform(lambda x:x.iloc[i])
        df_top[str(i+1) + '_cases'] = df_top.groupby('date').new_case.transform(lambda x:x.iloc[i])

    df_top = df_top.groupby('date').first().loc[:,'1':'5_cases']

    stacked = df_top.iloc[:,::2].stack().reset_index()
    stacked.head()

    df_top = pd.DataFrame(dict(country=df_top.values[:,::2].reshape(-1),
                          New_cases=df_top.values[:,1::2].reshape(-1),
                          Rank=stacked.level_1.values), index=stacked.date)

    df_top['Rank'] = np.where(df_top.Rank == '1', df_top.Rank+'st',
                                np.where(df_top.Rank == '2', df_top.Rank+'nd',
                                        np.where(df_top.Rank == '3', df_top.Rank+'rd',
                                                df_top.Rank+'th')))
    df_top = df_top.reset_index()

    country_list = coco.convert(names=df_top.country.to_list(), to='short_name', not_found=None)
    df_top['country'] = country_list
    try:
        dest = 'flags_top_bydate'
        copy_flag(dest, country_list)
    except:
        print("Copying flags to Tableau folder unsuccessful")

    return df_top


def country(df):
    df_country = df.reset_index().groupby(['date', 'country'], as_index=False).sum()

    country_list = coco.convert(names=df_country.country.to_list(), to='short_name', not_found=None)
    df_country['country'] = country_list
    df_country['continent'] = coco.convert(names=df_country.country.to_list(), to='continent')
    df_country['region'] = coco.convert(names=df_country.country.to_list(), to='UNregion')

    df_country_sort = df_country.groupby('country', as_index=False).sum().sort_values('new_case', ascending=False)
    df_country_sort.index = np.arange(1, len(df_country_sort) + 1)
    df_country_sort = df_country_sort.reset_index().loc[:, 'index':'country']

    df_country = pd.merge(df_country, df_country_sort, how='left', on='country')

    try:
        dest = 'flags_country'
        copy_flag(dest, country_list)
    except:
        print("Copying flags to Tableau folder unsuccessful")

    return df_country


def ratio(df):
    df_ratio = df.reset_index().groupby('country', as_index=False).sum()

    pop = pd.read_excel('data/population.xlsx')

    pop.Country = coco.convert(names=pop.Country.to_list(), to='short_name')
    pop.columns = ['country', 'population']

    country_list = coco.convert(names=df_ratio.country.to_list(), to='short_name', not_found=None)
    df_ratio['country'] = country_list

    df_ratio = pd.merge(df_ratio, pop, how='left', on='country')

    df_ratio['case_ratio'] = df_ratio.new_case / df_ratio.population
    
    try:
        dest = 'flags_ratio'
        copy_flag(dest, country_list)
    except:
        print("Copying flags to Tableau folder unsuccessful")

    return df_ratio


def china(df):
    df_china = df[df.country == 'China'].reset_index()

    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat_hubei = radians(df_china[df_china.location == 'Hubei'].iloc[0, 4])
    long_hubei = radians(df_china[df_china.location == 'Hubei'].iloc[0, 5])

    def distance_to_Hubei(row):
        lat = radians(row['lat'])
        long = radians(row['long'])

        dlong = long_hubei - long
        dlat = lat_hubei - lat

        a = sin(dlat / 2) ** 2 + cos(lat) * cos(lat_hubei) * sin(dlong / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    df_china['distance_hubei'] = df_china.apply(distance_to_Hubei, axis=1)

    return df_china


def age_ols():
    url_patient = 'https://docs.google.com/spreadsheets/d/1jS24DjSPVWa4iuxuD4OAXrE3QeI8c9BC1hSlqr-NMiU/edit#gid=1187587451'
    url_patient = url_patient.replace('/edit#gid=', '/export?format=csv&gid=')

    patient = pd.read_csv(url_patient, header=1, index_col=0)
    patient = patient[patient.age.notnull()]

    patient.death = np.where(patient.death == '0', 0, 1)

    import statsmodels.api as sm

    model = sm.OLS(patient.death, sm.add_constant(patient.age)).fit()
    age_coef = model.params['age']

    return age_coef


def kor_adjusted(df):
    last_date = df.index[-1]

    df_korea = df.reset_index().groupby(['date', 'country']).sum()
    df_korea = df_korea.loc[[last_date]].reset_index()

    df_korea['country'] = coco.convert(names=df_korea.country.to_list(), to='short_name', not_found=None)

    age = pd.read_csv('data/age.csv')
    age.country = coco.convert(names=age.country.to_list(), to='short_name')
    age.columns = ['country', 'age']

    df_korea = pd.merge(df_korea, age, how='left', on='country')

    age_coef = age_ols()

    kor = df_korea[df_korea.country == 'South Korea']
    kor_ratio = float(kor['cum_death'] / kor['cum_case'])
    kor_age = float(kor['age'])

    df_korea['age_diff_kor'] = df_korea.age - kor_age

    df_korea['cfr_adj'] = df_korea.age_diff_kor * age_coef / 4 + kor_ratio

    df_korea['cum_case_adj'] = np.where((df_korea.cum_case - df_korea.cum_death > 100) &
                                            (df_korea.cum_case < df_korea.cum_death / df_korea.cfr_adj),
                                            np.round(df_korea.cum_death / df_korea.cfr_adj, 0),
                                            df_korea.cum_case)
    df_korea['cum_case_diff'] = df_korea.cum_case_adj - df_korea.cum_case

    return df_korea
