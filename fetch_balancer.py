"""
Script to fetch all pools from Balancer using GraphQL API
"""
import requests
import json
from typing import List, Dict

def fetch_all_balancer_pools():
    """Fetch all pools from Balancer GraphQL API"""
    url = "https://api-v3.balancer.fi"
    
    all_pools = []
    skip = 0
    batch_size = 1000
    
    while True:
        query = """
        {
            pools(first: %d, skip: %d, where: {totalLiquidity_gt: "0"}) {
                id
                name
                symbol
                tokens {
                    id
                    symbol
                    name
                    balance
                    weight
                }
                totalLiquidity
                totalShares
                swapFee
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
            
            pools = data.get('data', {}).get('pools', [])
            
            if not pools:
                break
            
            all_pools.extend(pools)
            print(f"Fetched {len(pools)} pools (total: {len(all_pools)})")
            
            if len(pools) < batch_size:
                break
            
            skip += batch_size
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
    
    return all_pools

if __name__ == "__main__":
    print("Fetching all Balancer pools...")
    pools = fetch_all_balancer_pools()
    
    print(f"\nTotal pools fetched: {len(pools)}")
    
    if pools:
        print("\nFirst 5 pools:")
        for pool in pools[:5]:
            tokens_str = ", ".join([t.get('symbol', 'N/A') for t in pool.get('tokens', [])])
            print(f"  {pool.get('name', 'N/A')} ({pool.get('symbol', 'N/A')}) - Tokens: {tokens_str}")
        
        # Save to file
        with open('balancer_pools.json', 'w') as f:
            json.dump(pools, f, indent=2)
        print(f"\nData saved to balancer_pools.json")
