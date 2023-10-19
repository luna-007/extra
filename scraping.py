import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

url = 'https://data.sec.gov/submissions/CIK0001326801.json'

response = requests.get(url, headers=headers)

filings = json.loads(response.text)

print(filings['filings']['recent']['primaryDocument'])