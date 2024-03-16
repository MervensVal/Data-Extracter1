import requests as r
import db

def getCountryInfo():
    #country = 'United States of America'
    country = 'France'
    response = r.get('https://restcountries.com/v3.1/name/'+country)
    data = response.json()
    capital = (str(data[0]['capital']).replace("['","")).replace("']","")
    region = (str(data[0]['region']).replace("['","")).replace("']","")
    subregion = (str(data[0]['subregion']).replace("['","")).replace("']","")
    landlocked = (str(data[0]['landlocked']).replace("['","")).replace("']","")
    currency = (str(data[0]['currencies']))
    db.InsertCountryInfo(country,capital,region,subregion,landlocked,currency)
    print('-----------------------')
    print('Country Data')
    print(f'capital {capital}')
    print(f'region {region}')
    print(f'subregion {subregion}')
    print(f'landlocked {landlocked}')
    print(f'currency {currency}')

    

