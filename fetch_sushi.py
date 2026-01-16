"""
Script to fetch all trading pairs from SushiSwap using Subgraph API
"""
import requests
import json
from typing import List, Dict

def fetch_all_sushi_pairs():
    """Fetch all trading pairs from SushiSwap Subgraph"""
    url = "https://api.thegraph.com/subgraphs/name/sushiswap/exchange"
    
    all_pairs = []
    skip = 0
    batch_size = 1000
    
    while True:
        query = """
        {
            pairs(first: %d, skip: %d, where: {reserveUSD_gt: "0"}) {
                id
                token0 {
                    id
                    symbol
                    name
                }
                token1 {
                    id
                    symbol
                    name
                }
                reserve0
                reserve1
                reserveUSD
                token0Price
                token1Price
                volumeUSD
            }
        }
        """ % (batch_size, skip)
        
        try:
            response = requests.post(url, json={'query': query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                print(f"GraphQL errors: {data['errors']}")
                break
            
            pairs = data.get('data', {}).get('pairs', [])
            
            if not pairs:
                break
            
            all_pairs.extend(pairs)
            print(f"Fetched {len(pairs)} pairs (total: {len(all_pairs)})")
            
            if len(pairs) < batch_size:
                break
            
            skip += batch_size
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
    
    return all_pairs

if __name__ == "__main__":
    print("Fetching all SushiSwap pairs...")
    pairs = fetch_all_sushi_pairs()
    
    print(f"\nTotal pairs fetched: {len(pairs)}")
    
    if pairs:
        print("\nFirst 5 pairs:")
        for pair in pairs[:5]:
            print(f"  {pair['token0']['symbol']}/{pair['token1']['symbol']} - Price: {pair.get('token0Price', 'N/A')}")
        
        # Save to file
        with open('sushi_pairs.json', 'w') as f:
            json.dump(pairs, f, indent=2)
        print(f"\nData saved to sushi_pairs.json")
