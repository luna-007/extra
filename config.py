import requests, websocket
import json
from secret import SECRET_KEY

# extra = '101-001-26758755-001'
extra = '101-001-26758755-001'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + SECRET_KEY,
}

params = {
    'instruments': 'EUR_USD,USD_CAD',
}

response = requests.get(f'https://stream-fxpractice.oanda.com/v3/accounts/{extra}/transactions/stream', headers=headers)

data = json.loads(response.text)
print(data) 
# for i in range(len(data['instruments'])):
#     print(data['instruments'][i]['displayName'] + ' ' + data['instruments'][i]['name'])

# print(data['instruments'][1]['displayName'])