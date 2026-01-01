
import requests
import json
import sys

BASE_URL = "http://localhost:8888/api/v1"

def test_endpoint(endpoint_name):
    print(f"Testing {endpoint_name}...")
    try:
        response = requests.get(f"{BASE_URL}/{endpoint_name}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            # print(json.dumps(data, indent=2))
            key = 'cases' if 'cases' in endpoint_name else 'news'
            items = data.get(key, [])
            print(f"Success! Found {len(items)} items.")
            if len(items) > 0:
                print(f"Sample Item: {items[0].get('title')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Connection Failed: {e}")
        return False

print("--- DIAGNOSTIC START ---")
cases_ok = test_endpoint("major-cases")
news_ok = test_endpoint("legal-news")
print("--- DIAGNOSTIC END ---")

if cases_ok and news_ok:
    print("BACKEND IS WORKING FINE.")
else:
    print("BACKEND ISSUE DETECTED.")
