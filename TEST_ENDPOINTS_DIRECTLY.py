"""
Quick test script to verify the endpoints return data
Run this while server is running: python TEST_ENDPOINTS_DIRECTLY.py
"""
import requests
import json

BASE_URL = "http://localhost:8888/api/v1"

print("Testing Major Cases endpoint...")
try:
    response = requests.get(f"{BASE_URL}/major-cases", timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Cases returned: {len(data.get('cases', []))}")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

print("Testing Legal News endpoint...")
try:
    response = requests.get(f"{BASE_URL}/legal-news", timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"News returned: {len(data.get('news', []))}")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

