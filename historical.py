import requests
from keys import *
import json

url = "https://api-testnet.bybit.com/v5/order/realtime"

payload={}
headers = {
  'X-BAPI-API-KEY': API_KEY,
  'X-BAPI-TIMESTAMP': '1693939221624',
  'X-BAPI-RECV-WINDOW': '20000',
  'X-BAPI-SIGN': '39ef95f35a13d44dbc204caddac1c41058b452f87ec5fd905a16dd8cfd1faaef'
}

response = requests.request(url, headers=headers, data=payload)
# data = json.loads(response.text)

print(response.text)