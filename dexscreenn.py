import requests
import json
from collections import defaultdict

with open('cryptocurrencies.json') as f:
    coins = json.load(f)['cryptocurrencies']

with open('exchanges.json') as f:
    dex_list = [ex['name'].lower() for ex in json.load(f)['exchanges']]

base_url = "https://api.dexscreener.com/latest/dex"
# Группируем по валютным парам: {pair: [{dex, price, chain, vol}]}
pairs_data = defaultdict(list)

print("Сравнение цен относительно USDT:\n")

for coin in coins[:20]:
    try:
        url = f"{base_url}/search?q={coin}"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        for p in data.get('pairs', []):
            chain = p.get('chainId', '').lower()
            dex = p.get('dexId', '').lower()
            base = p.get('baseToken', {}).get('symbol', '').upper()
            quote = p.get('quoteToken', {}).get('symbol', '').upper()
            
            # Ищем пары с USDT
            is_usdt = quote == 'USDT'
            is_our_dex = any(d in dex for d in dex_list) or dex in ['uniswap', 'sushiswap', 'pancakeswap', 'quickswap', 'balancer', '1inch', 'raydium', 'camelot', 'aerodrome', 'traderjoe']
            
            if is_usdt and is_our_dex:
                price = float(p.get('priceUsd', 0))
                if price > 0:
                    pair_key = f"{base}/USDT"
                    pairs_data[pair_key].append({
                        'dex': dex,
                        'chain': chain,
                        'price': price,
                        'vol': p.get('volume', {}).get('h24', 0),
                        'url': p.get('url', '')
                    })
        import time
        time.sleep(0.3)
    except:
        pass

# Выводим результаты
for pair, exchanges in pairs_data.items():
    if len(exchanges) < 2:
        continue  # Показываем только если есть на нескольких биржах
    
    # Сортируем по цене
    sorted_ex = sorted(exchanges, key=lambda x: x['price'])
    min_price = sorted_ex[0]['price']
    max_price = sorted_ex[-1]['price']
    diff = ((max_price - min_price) / min_price * 100) if min_price > 0 else 0
    
    print(f"{pair}:")
    print(f"  MIN: ${min_price:.6f} | MAX: ${max_price:.6f} | Разница: {diff:.2f}%")
    
    # Сортируем: сначала Polygon, потом по цене
    polygon_first = sorted(exchanges, key=lambda x: (x['chain'] != 'polygon', x['price']))
    
    for ex in polygon_first:
        marker = ""
        if ex['price'] == min_price:
            marker = " [MIN]"
        elif ex['price'] == max_price:
            marker = " [MAX]"
        
        chain_marker = " [POLYGON]" if ex['chain'] == 'polygon' else ""
        url = ex.get('url', '')
        url_str = f" | {url}" if url else ""
        print(f"    {ex['dex']:20} ({ex['chain']:10}) ${ex['price']:>10.6f}{marker}{chain_marker}{url_str}")
    print()
