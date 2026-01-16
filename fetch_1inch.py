"""
Script to fetch tokens and prices from 1inch API
"""
import requests
import json
from typing import List, Dict

def fetch_1inch_tokens(chain_id=1):
    """Fetch all tokens from 1inch API for a specific chain"""
    # Chain IDs: 1=Ethereum, 56=BSC, 137=Polygon, etc.
    url = f"https://api.1inch.dev/token/v1.2/{chain_id}/tokens"
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tokens: {e}")
        return None

def fetch_1inch_spot_prices(chain_id=1, tokens=None):
    """Fetch spot prices for tokens"""
    if not tokens:
        tokens_data = fetch_1inch_tokens(chain_id)
        if tokens_data and 'tokens' in tokens_data:
            tokens = list(tokens_data['tokens'].keys())[:10]  # Limit to first 10 for testing
    
    if not tokens:
        return None
    
    url = f"https://api.1inch.dev/price/v1.1/{chain_id}"
    
    # Build query string with token addresses
    params = {
        'tokens': ','.join(tokens),
        'currency': 'USD'
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching spot prices: {e}")
        return None

if __name__ == "__main__":
    print("Fetching 1inch tokens and prices...")
    
    # Try Ethereum mainnet (chain_id=1)
    print("\n1. Fetching tokens for Ethereum (chain_id=1)...")
    tokens = fetch_1inch_tokens(chain_id=1)
    
    if tokens:
        if 'tokens' in tokens:
            token_count = len(tokens['tokens'])
            print(f"Total tokens: {token_count}")
            
            # Show first 5 tokens
            print("\nFirst 5 tokens:")
            for i, (addr, token_info) in enumerate(list(tokens['tokens'].items())[:5]):
                print(f"  {token_info.get('symbol', 'N/A')} ({token_info.get('name', 'N/A')})")
            
            # Try to get prices for first few tokens
            print("\n2. Fetching spot prices...")
            token_addresses = list(tokens['tokens'].keys())[:10]
            prices = fetch_1inch_spot_prices(chain_id=1, tokens=token_addresses)
            
            if prices:
                print(f"Got prices for {len(prices)} tokens")
                print("\nSample prices:")
                for addr, price_data in list(prices.items())[:5]:
                    token_symbol = tokens['tokens'].get(addr, {}).get('symbol', addr[:10])
                    print(f"  {token_symbol}: ${price_data.get('price', 'N/A')}")
            
            # Save to file
            with open('1inch_tokens.json', 'w') as f:
                json.dump(tokens, f, indent=2)
            print(f"\nData saved to 1inch_tokens.json")
        else:
            print(f"Response structure: {json.dumps(tokens, indent=2)[:500]}")
    else:
        print("Failed to fetch tokens")
