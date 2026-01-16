"""
Script to fetch all trading pairs from Raydium AMM using REST API
"""
import requests
import json
from typing import List, Dict

def fetch_all_raydium_pools():
    """Fetch all pools from Raydium API"""
    base_url = "https://api-v3.raydium.io"
    
    # Try different possible endpoints
    endpoints_to_try = [
        "/pools",
        "/pools/all",
        "/pools/mainnet",
        "/v3/pools",
        "/ammPools"
    ]
    
    for endpoint in endpoints_to_try:
        url = f"{base_url}{endpoint}"
        print(f"Trying endpoint: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check if we got valid data
            if isinstance(data, (list, dict)):
                print(f"Success! Got data from {endpoint}")
                return data, endpoint
            else:
                print(f"Unexpected response format from {endpoint}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error with {endpoint}: {e}")
            continue
    
    return None, None

if __name__ == "__main__":
    print("Fetching all Raydium pools...")
    pools, endpoint = fetch_all_raydium_pools()
    
    if pools:
        if isinstance(pools, list):
            print(f"\nTotal pools fetched: {len(pools)}")
            print(f"\nFirst 5 pools:")
            for pool in pools[:5]:
                print(f"  {json.dumps(pool, indent=2)[:200]}...")
        else:
            print(f"\nResponse structure:")
            print(json.dumps(pools, indent=2)[:500])
        
        # Save to file
        with open('raydium_pools.json', 'w') as f:
            json.dump(pools, f, indent=2)
        print(f"\nData saved to raydium_pools.json")
    else:
        print("\nFailed to fetch data from any endpoint")
