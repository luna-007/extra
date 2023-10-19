import requests
import json

url = 'https://www.sec.gov/files/company_tickers.json'

response = requests.get(url)
data = json.loads(response.text)

def get_symbols(value):
    stock_list = {}
    for key in value:
        stock_list[value[key]['cik_str']] = value[key]['ticker']
    return stock_list

stock_data = get_symbols(data)

for i in stock_data:
    # print("CIK:", i, "Symbol:", stock_data[i])
    if stock_data[i] == 'META':
        print("The search result you are looking for")
        print("CIK:", i, "Symbol:", stock_data[i])