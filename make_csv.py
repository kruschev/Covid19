import numpy as np
import pandas as pd
import country_converter as coco

# This function will copy the flags to be shown on the Tableau's visuals
def copy_flag(dest, country_list, ship=True):
    import os, shutil
    import config

    path = 'tableau/flags'
    dest = config.dir + dest

    files = os.listdir(path)
    shutil.rmtree(dest, ignore_errors=True) #remove existing flag folder
    os.mkdir(dest) #remake a new folder

    for file in files:
        if ship:
            country_name = coco.convert(names=file.split('.')[0], to='short_name', not_found=None) #convert country names to standard name
        else:
            country_name = coco.convert(names=file.split('.')[0], to='short_name')
            
        if country_name in country_list: #Copy the country flags if they are in the dataset
            src = os.path.join(path, file)
            shutil.copy(src, dest)
            if country_name == 'DR Congo': #the capitalized R in DR is problematic for Tableau
                os.rename(os.path.join(dest, file), os.path.join(dest, 'Dr Congo.png'))
            elif country_name == 'MS Zaandam': #the capitalized S in MS is problematic for Tableau
                os.rename(os.path.join(dest, file), os.path.join(dest, 'Ms Zaandam.png'))
            else:
                os.rename(os.path.join(dest, file), os.path.join(dest, country_name + '.png'))

    return


# This function is for the weekly new cases ranking chart
def top_bydate(df):
    df_top = df.groupby([pd.Grouper(freq='W', level=0), 'country']).sum() #group the data by date (weekly) and then by country
    df_top = df_top.reset_index()
    df_top = df_top.sort_values(['date', 'new_case'], ascending=[True, False])

    for i in range(5): #preparing the ranking
        df_top[str(i+1)] = df_top.groupby('date').country.transform(lambda x:x.iloc[i]) #top 5 countries
        df_top[str(i+1) + '_cases'] = df_top.groupby('date').new_case.transform(lambda x:x.iloc[i]) #number of new cases associated with such country

    df_top = df_top.groupby('date').first().loc[:,'1':'5_cases'] #keep only the relevant columns

    stacked = df_top.iloc[:,::2].stack().reset_index() #transform the df

    df_top = pd.DataFrame(dict(country=df_top.values[:,::2].reshape(-1),
                          New_cases=df_top.values[:,1::2].reshape(-1),
                          Rank=stacked.level_1.values), index=stacked.date)

    #rename the ranking for displaying in Tableau
    df_top['Rank'] = np.where(df_top.Rank == '1', df_top.Rank+'st',
                                np.where(df_top.Rank == '2', df_top.Rank+'nd',
                                        np.where(df_top.Rank == '3', df_top.Rank+'rd',
                                                df_top.Rank+'th')))
    df_top = df_top.reset_index()

    country_list = coco.convert(names=df_top.country.to_list(), to='short_name', not_found=None) #convert country names to standard
    df_top['country'] = country_list
    try:
        dest = 'flags_top_bydate'
        copy_flag(dest, country_list)
    except:
        print("Copying flags to Tableau folder unsuccessful")

    return df_top


# This function is for creating the main data for various charts
def country(df):
    df_country = df.reset_index().groupby(['date', 'country'], as_index=False).sum() #group the data by date (daily) and then country

    country_list = coco.convert(names=df_country.country.to_list(), to='short_name', not_found=None) #convert country names to standard
    df_country['country'] = country_list
    df_country['continent'] = coco.convert(names=df_country.country.to_list(), to='continent')

    #this dataframe is for creating a ranking column based on total confirmed cases, which is helpful in Tableau
    df_country_sort = df_country.groupby('country', as_index=False).sum().sort_values('new_case', ascending=False)
    df_country_sort.index = np.arange(1, len(df_country_sort) + 1)
    df_country_sort = df_country_sort.reset_index().loc[:, 'index':'country']

    df_country = pd.merge(df_country, df_country_sort, how='left', on='country') #merge with main dataframe

    try:
        dest = 'flags_country'
        copy_flag(dest, country_list)
    except:
        print("Copying flags to Tableau folder unsuccessful")

    return df_country


# This function is for the Case per capita chart
def ratio(df):
    df_ratio = df.reset_index().groupby('country', as_index=False).sum() #group the data by country (date is not considered)

    pop = pd.read_excel('data/population.xlsx') #data for country's population

    pop.Country = coco.convert(names=pop.Country.to_list(), to='short_name') #convert country names
    pop.columns = ['country', 'population'] #rename columns

    country_list = coco.convert(names=df_ratio.country.to_list(), to='short_name', not_found=None) #convert country names
    df_ratio['country'] = country_list

    df_ratio = pd.merge(df_ratio, pop, how='left', on='country') #merge with main df

    df_ratio['case_ratio'] = df_ratio.new_case / df_ratio.population #calculate the case per capita ratio
    
    try:
        dest = 'flags_ratio'
        copy_flag(dest, country_list, ship=False)
    except:
        print("Copying flags to Tableau folder unsuccessful")

    return df_ratio


# This function is for the China chart
def china(df):
    df_china = df[df.country == 'China'].reset_index()

    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat_hubei = radians(df_china[df_china.location == 'Hubei'].iloc[0, 3])
    long_hubei = radians(df_china[df_china.location == 'Hubei'].iloc[0, 4])

    # calculate the distance from each province to Hubei, in km
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


# This function is for the kor_adjusted function
def age_ols():
    #data contains information of Covid-19 patients
    url_patient = 'https://docs.google.com/spreadsheets/d/1jS24DjSPVWa4iuxuD4OAXrE3QeI8c9BC1hSlqr-NMiU/edit#gid=1187587451'
    url_patient = url_patient.replace('/edit#gid=', '/export?format=csv&gid=')

    patient = pd.read_csv(url_patient, header=1, index_col=0)
    patient = patient[patient.age.notnull()] #excluding data without age

    patient.death = np.where(patient.death == '0', 0, 1) #encoding the death status (1=deceased, 0=recovered/in treatment)

    import statsmodels.api as sm

    model = sm.OLS(patient.death, sm.add_constant(patient.age)).fit() #run a regression model of age on fatality
    age_coef = model.params['age'] #get the coefficent of age

    return age_coef


# This function is for the estimated real total cases chart
def kor_adjusted(df):
    last_date = df.index[-1] #select only the last date in the data

    df_korea = df.reset_index().groupby(['date', 'country']).sum()
    df_korea = df_korea.loc[[last_date]].reset_index()

    df_korea['country'] = coco.convert(names=df_korea.country.to_list(), to='short_name', not_found=None) #convert country names

    age = pd.read_csv('data/age.csv') #data for country's average age
    age.country = coco.convert(names=age.country.to_list(), to='short_name') #convert country names
    age.columns = ['country', 'age']

    df_korea = pd.merge(df_korea, age, how='left', on='country') #merge with df

    age_coef = age_ols() #get the age coefficent

    #get the case fatality rate (cfr) for South Korea, and its average age
    kor = df_korea[df_korea.country == 'South Korea']
    kor_ratio = float(kor['cum_death'] / kor['cum_case'])
    kor_age = float(kor['age'])

    df_korea['age_diff_kor'] = df_korea.age - kor_age #calculate the age difference to South Korea

    #calculate the adjusted cfr for each country. Age data is shown in range of 4 years, thus the division.
    df_korea['cfr_adj'] = df_korea.age_diff_kor * age_coef / 4 + kor_ratio

    #calculate the adjusted total cases
    #First condition is for avoiding adjustment for countries with too few deaths (not enough confidence).
    #Second condition is for avoiding reducing total cases, if reported number is already higher than estimation.
    df_korea['cum_case_adj'] = np.where((df_korea.cum_case - df_korea.cum_death > 100) &
                                            (df_korea.cum_case < df_korea.cum_death / df_korea.cfr_adj),
                                            np.round(df_korea.cum_death / df_korea.cfr_adj, 0),
                                            df_korea.cum_case)
    df_korea['cum_case_diff'] = df_korea.cum_case_adj - df_korea.cum_case

    return df_korea
