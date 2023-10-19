import requests
from keys import *
import json

HEADERS = {
    f"APCA-API-KEY-ID: {API_KEY}",
    f"APCA-API-SECRET-KEY: {SECRET_KEY}"
}

url = "https://data.alpaca.markets/v1beta1/news?sort=desc"

headers = {"accept": "application/json"}

response = requests.get(url, headers=HEADERS)

print(json.loads(response.content))