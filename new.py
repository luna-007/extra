import requests

response = requests.get('https://api.db.nomics.world/v22/datasets/IMF/WEO:latest')

print(response.text)