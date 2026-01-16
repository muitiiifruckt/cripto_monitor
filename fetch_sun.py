"""
Script to fetch trading pairs from SUN - testing various endpoints
"""
import requests
import json
from typing import List, Dict

def test_sun_endpoints():
    """Test various possible endpoints for SUN API"""
    base_url = "https://api.sunswap.com"
    
    endpoints_to_try = [
        "/pairs",
        "/markets",
        "/pools",
        "/tickers",
        "/v1/pairs",
        "/v1/markets",
        "/pairs/all",
        "/markets/all"
    ]
    
    for endpoint in endpoints_to_try:
        url = f"{base_url}{endpoint}"
        print(f"Trying endpoint: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Success! Got data: {type(data)}")
                    if isinstance(data, list):
                        print(f"  List length: {len(data)}")
                    elif isinstance(data, dict):
                        print(f"  Dict keys: {list(data.keys())[:5]}")
                    return data, endpoint
                except:
                    print(f"  Response is not JSON: {response.text[:200]}")
            else:
                print(f"  Response: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}")
    
    return None, None

if __name__ == "__main__":
    print("Testing SUN API endpoints...")
    data, endpoint = test_sun_endpoints()
    
    if data:
        print(f"\nSuccessfully fetched data from {endpoint}")
        print(f"Data preview: {json.dumps(data, indent=2)[:500]}")
        
        with open('sun_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nData saved to sun_data.json")
    else:
        print("\nFailed to fetch data from any endpoint")
