import requests as r

def getCountryInfo(country):
    response = r.get('https://restcountries.com/v3.1/name/'+country)
    print(f' Status for {str(country)} data retrieval: {response.status_code}')
    return response