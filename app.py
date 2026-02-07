import requests
from bs4 import BeautifulSoup
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🛡️ User-Agent Pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

# 🌐 Function to get fresh free proxies
def get_free_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        resp = requests.get(url)
        proxies = resp.text.split('\r\n')
        return [p for p in proxies if p]
    except:
        return []

@app.route('/api/google', methods=['GET'])
def google_scraper():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Search query missing!"})

    proxies_list = get_free_proxies()
    url = f"https://www.google.com/search?q={query}&num=10&hl=en"
    
    # Retry logic: Agar aik proxy fail ho toh dusri try karo
    for i in range(5):  # Max 5 retries
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        proxy_config = None
        
        if proxies_list:
            proxy = random.choice(proxies_list)
            proxy_config = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        
        try:
            # Proxy ke sath request bhejna
            response = requests.get(url, headers=headers, proxies=proxy_config, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []

                for g in soup.select('.tF2Cxc'):
                    title = g.select_one('h3')
                    link = g.select_one('a')
                    snippet = g.select_one('.VwiC3b')

                    if title and link:
                        results.append({
                            "title": title.get_text(),
                            "link": link['href'],
                            "description": snippet.get_text() if snippet else "No description"
                        })

                if results:
                    return jsonify({
                        "status": True,
                        "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐏𝐑𝐎 𝐒𝐂𝐑𝐀𝐏𝐄𝐑",
                        "proxy_used": proxy if proxy_config else "Direct IP",
                        "results": results
                    })
        
        except Exception as e:
            print(f"Proxy {proxy} failed, retrying...")
            continue

    return jsonify({"status": False, "msg": "Google is blocking all requests right now. Try again later."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
