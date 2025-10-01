import requests
import openai
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("POLYGON_API_KEY")

print(f"API Key loaded: {API_KEY is not None}")

if not API_KEY:
    print("ERROR: API_KEY is None. Make sure to set POLYGON_API_KEY in your .env file")
    exit(1)

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={API_KEY}"
print(f"Making request to: {url}")

response = requests.get(url)
print(f"Response status code: {response.status_code}")

if response.status_code != 200:
    print(f"ERROR: API request failed with status {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

data = response.json()
print(f"Response keys: {list(data.keys())}")

tickers = []

# Process the first page of results
if 'results' in data:
    print(f"First page has {len(data['results'])} tickers")
    for ticker in data['results']:
        tickers.append(ticker)
else:
    print("No 'results' key in response")
    print(f"Full response: {data}")

# Process additional pages if they exist
while 'next_url' in data:
    print(f"Fetching next page: {data['next_url']}")
    response = requests.get(data['next_url'] + f"&apiKey={API_KEY}")
    
    if response.status_code != 200:
        print(f"ERROR: Pagination request failed with status {response.status_code}")
        break
        
    data = response.json()
    
    if 'results' in data:
        print(f"Next page has {len(data['results'])} tickers")
        for ticker in data['results']:
            tickers.append(ticker)
    else:
        print("No 'results' key in pagination response")
        break

print(f"Total tickers collected: {len(tickers)}")