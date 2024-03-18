import requests as r
import db

def getCountryInfo(country):
    response = r.get('https://restcountries.com/v3.1/name/'+country)
    return response

    

