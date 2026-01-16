"""
Test script to check API connectivity and endpoints
"""
import requests
import json

def test_uniswap_subgraph():
    """Test Uniswap Subgraph connection"""
    print("=" * 60)
    print("Testing Uniswap Subgraph...")
    print("=" * 60)
    
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
    
    # Simple query to test connection
    query = """
    {
        pairs(first: 5) {
            id
            token0 {
                symbol
            }
            token1 {
                symbol
            }
        }
    }
    """
    
    try:
        print(f"URL: {url}")
        print(f"Query: {query.strip()}")
        print("\nSending request...")
        
        response = requests.post(
            url, 
            json={'query': query}, 
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nResponse received!")
            
            if 'errors' in data:
                print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
            else:
                pairs = data.get('data', {}).get('pairs', [])
                print(f"Success! Got {len(pairs)} pairs")
                print(f"Sample data: {json.dumps(pairs[:2], indent=2)}")
                return True
        else:
            print(f"Error: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
        return False

def test_raydium_api():
    """Test Raydium API connection"""
    print("\n" + "=" * 60)
    print("Testing Raydium API...")
    print("=" * 60)
    
    endpoints = [
        "https://api-v3.raydium.io/pools",
        "https://api-v3.raydium.io/main/pools",
        "https://api-v3.raydium.io/ammPools"
    ]
    
    for url in endpoints:
        try:
            print(f"\nTrying: {url}")
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Response type: {type(data)}")
                if isinstance(data, list):
                    print(f"Got {len(data)} items")
                elif isinstance(data, dict):
                    print(f"Keys: {list(data.keys())[:5]}")
                print(f"Sample: {str(data)[:200]}")
                return True
            else:
                print(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")
    
    return False

def test_1inch_api():
    """Test 1inch API connection"""
    print("\n" + "=" * 60)
    print("Testing 1inch API...")
    print("=" * 60)
    
    url = "https://api.1inch.dev/token/v1.2/1/tokens"
    
    try:
        print(f"URL: {url}")
        response = requests.get(
            url,
            headers={"Accept": "application/json"},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'tokens' in data:
                print(f"Success! Got {len(data['tokens'])} tokens")
                return True
            else:
                print(f"Response: {json.dumps(data, indent=2)[:500]}")
        else:
            print(f"Error: {response.text[:500]}")
    except Exception as e:
        print(f"Exception: {e}")
    
    return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("API CONNECTION TESTS")
    print("=" * 60 + "\n")
    
    results = {
        "Uniswap": test_uniswap_subgraph(),
        "Raydium": test_raydium_api(),
        "1inch": test_1inch_api()
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for exchange, result in results.items():
        status = "✓ SUCCESS" if result else "✗ FAILED"
        print(f"{exchange}: {status}")
