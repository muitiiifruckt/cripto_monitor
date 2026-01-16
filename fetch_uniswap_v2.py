"""
Improved script to fetch all trading pairs from Uniswap with better error handling
"""
import requests
import json
import time

def fetch_uniswap_pairs_improved():
    """Fetch all trading pairs from Uniswap with multiple endpoint attempts"""
    
    # Try different possible Subgraph endpoints
    endpoints = [
        "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
        "https://gateway.thegraph.com/api/subgraphs/id/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco",
        "https://subgraph.satsuma-prod.com/09c1730c7e46/uniswap/uniswap-v2/api"
    ]
    
    all_pairs = []
    
    for endpoint_url in endpoints:
        print(f"\n{'='*60}")
        print(f"Trying endpoint: {endpoint_url}")
        print(f"{'='*60}")
        
        skip = 0
        batch_size = 100
        
        # Start with smaller batch to test
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
                }
            }
            """ % (batch_size, skip)
            
            try:
                print(f"\nRequest: skip={skip}, batch_size={batch_size}")
                
                response = requests.post(
                    endpoint_url,
                    json={'query': query},
                    headers={
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    timeout=30
                )
                
                print(f"Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"Error: {response.text[:500]}")
                    break
                
                data = response.json()
                
                if 'errors' in data:
                    print(f"GraphQL Errors:")
                    for error in data['errors']:
                        print(f"  - {json.dumps(error, indent=2)}")
                    break
                
                pairs = data.get('data', {}).get('pairs', [])
                
                if not pairs:
                    print("No more pairs")
                    break
                
                all_pairs.extend(pairs)
                print(f"✓ Got {len(pairs)} pairs (total: {len(all_pairs)})")
                
                if len(pairs) < batch_size:
                    print("Reached end")
                    break
                
                skip += batch_size
                time.sleep(0.5)  # Rate limiting
                
            except requests.exceptions.Timeout:
                print(f"✗ Timeout")
                break
            except requests.exceptions.ConnectionError as e:
                print(f"✗ Connection error: {e}")
                break
            except Exception as e:
                print(f"✗ Error: {type(e).__name__}: {e}")
                break
        
        if all_pairs:
            print(f"\n✓ Successfully fetched {len(all_pairs)} pairs from {endpoint_url}")
            return all_pairs
    
    return all_pairs

if __name__ == "__main__":
    print("\n" + "="*60)
    print("UNISWAP PAIRS FETCHER (Improved)")
    print("="*60)
    
    pairs = fetch_uniswap_pairs_improved()
    
    print("\n" + "="*60)
    print(f"TOTAL PAIRS: {len(pairs)}")
    print("="*60)
    
    if pairs:
        print("\nFirst 5 pairs:")
        for i, pair in enumerate(pairs[:5], 1):
            token0 = pair.get('token0', {}).get('symbol', 'N/A')
            token1 = pair.get('token1', {}).get('symbol', 'N/A')
            price = pair.get('token0Price', 'N/A')
            print(f"  {i}. {token0}/{token1} - Price: {price}")
        
        try:
            with open('uniswap_pairs.json', 'w', encoding='utf-8') as f:
                json.dump(pairs, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Saved to uniswap_pairs.json")
        except Exception as e:
            print(f"\n✗ Save error: {e}")
    else:
        print("\n✗ No pairs fetched")
