
    # In[1]:


#Import Dependencies
import pandas as pd
from sqlalchemy import create_engine


    # In[3]:

def scrape():
    df=pd.read_csv("../SecondProject2/Resources/Project2_idmc_disaster_all_dataset.csv")
    df.head()


    # In[4]:


    import pycountry_convert as pc


    # In[5]:


    country_code = pc.country_name_to_country_alpha2("China", cn_name_format="default")
    print(country_code)
    continent_name = pc.country_alpha2_to_continent_code(country_code)
    print(continent_name)


    # In[6]:


    def country_code(name):
        try:
            code = pc.country_name_to_country_alpha2(name, cn_name_format="default")
            return code
        except:
            return "N/A"
    def continent_name(name):
        try:
            continent = pc.country_alpha2_to_continent_code(name)
            return continent
        except:
            return "N/A"
    df["Country_2D"] = df["Country Name"].apply(country_code)
    df["Continent"] = df["Country_2D"].apply(continent_name)


    # In[7]:


    df.head()


    # In[8]:


    df_Africa= df[df["Continent"]=="AF"]
    df_Africa.head()


    # In[9]:


    df_africa = df_Africa.rename(columns = {'Country Name': 'Country',})
    df_africa.head()


    # In[10]:


    df_africa.columns


    # In[11]:


    df.groupby("Continent").count()


    # In[12]:


    #Import Dependencies
    import os
    import requests
    import json
    import pprint
    import numpy as np
    import flask
    import wbdata
    import datetime

    # In[13]:


    countries = ['algeria', 'angola', 'benin', 'botswana', 'burkina faso', 'burundi', 'cabo verde',
                'cameroon', 'central african republic', 'chad', 'comoros', 'congo', "cote d'ivoire",
                'djibouti', 'egypt', 'equatorial guinea', 'esqtini', 'ethiopia', 'gabon', 'gambia',
                'ghana', 'guinea', 'guinea-bissau', 'kenya', 'lesotho', 'liberia', 'libya', 'madagascar',
                'malawi', 'mali', 'mauritania', 'mauritius', 'morocco', 'mozambique', 'namibia', 'niger',
                'nigeria', 'rwanda', 'sao tome and principe', 'senegal', 'seychelles', 'sirre leone',
                'somalia', 'south africa', 'south sudan', 'sudan', 'tanzania', 'togo', 'tunisia', 
                'uganda', 'zambia', 'zimbabwe']
    country_codes = ['AGO', 'ALB', 'ARB', 'BDI', 'BEN', 'BFA', 'BMN', 'BSS', 'BWA', 'CAA', 'CAF',
                    'CIV', 'CME', 'CMR', 'COG', 'COM', 'CPV', 'DJI', 'DMN', 'DSF', 'DSS', 'DZA',
                    'EGY', 'ETH', 'GAB', 'GHA', 'GMB', 'GNB', 'GNQ', 'KEN', 'LBR', 'LSO', 'MAR',
                    'MDG', 'MEA', 'MLI', 'MNA', 'MOZ', 'MRT', 'MUS', 'MWI', 'NAF', 'NAM', 'NER',
                    'NGA', 'NLS', 'NRS', 'RRS', 'RSO', 'RWA', 'SDN', 'SLE', 'SOM', 'SSA', 'SSD',
                    'SSF', 'SWZ', 'SXZ', 'SYC', 'TCD', 'TGO', 'TMN', 'TSS', 'TUN', 'TZA', 'UGA',
                    'XZN', 'ZAF', 'ZMB', 'ZWE']
    indicators = "SP.POP.TOTL"
    data_date = datetime.datetime(2008, 1, 1), datetime.datetime(2019, 1, 1)
    wbdata.get_indicator(source=50)


    # In[14]:


    wbdata.search_countries('')


    # In[15]:


    data = wbdata.get_data(indicators, country = country_codes, data_date = data_date)
    df_wbdata = pd.DataFrame(data)
    df_wbdata = df_wbdata.rename(columns={"indicator": "Indicator", 
                    "country": "Country",
                    "countryiso3code": "Country code",
                    "date": "Year",
                    "value": "Population",})
    df_wbdata = df_wbdata.filter(items = ['Country', 'Country code', 'Year', 'Population'])
    df_wbdata.dropna(inplace=True)
    df_wbdata['Country'] = df_wbdata['Country'].astype(str)
    df_wbdata['Country code'] = df_wbdata['Country code'].astype(str)
    df_wbdata['Year'] = df_wbdata['Year'].astype(str)
    df_wbdata['Population'] = df_wbdata['Population'].astype(str)
    df_wbdata['Country'] = df_wbdata['Country'].str.slice(23, -2)
    df_wbdata


    # In[16]:


    df_africa['Year'] = df_africa['Year'].astype('int64')
    df_wbdata['Year'] = df_wbdata['Year'].astype('int64')


    # In[17]:


    merged_df = pd.merge (left = df_africa, right = df_wbdata, how = "left", on=['Country code','Year', 'Country'])
    merged_df.head()


    # In[18]:


    merged_df = merged_df.rename(columns={'Country code': 'Country_Code',
                            'Start Date': 'Start_Date',
                            'Event Name': 'Event_Name',
                            'Hazard Category': 'Hazard_Category',
                            'Hazard Type': 'Hazard_Type',
                            'New Displacements': 'New_Displacements',})
    merged_df.head()

    merged_df = merged_df.dropna()
    merged_df

    merged_df[merged_df['Population'].isna()].count()
    merged_df.to_csv('merged.csv', index = False)

    #Create the engine and pass in Postgresql
    engine = create_engine('postgresql://postgres:TL!ttl310@localhost/project2_db')

    engine.table_names()

    query = pd.read_sql_query('select * from merged_data', con=engine)

    return(query)

if __name__ == '__main__':
    scrape()



