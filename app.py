import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# 🛡️ Real Browser Headers (Taake hum insaan lagen)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
]

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐒𝐄𝐀𝐑𝐂𝐇 𝐄𝐍𝐆𝐈𝐍𝐄 - HTML VERSION"

@app.route('/api/search', methods=['GET'])
def search_engine():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    # 🚀 DuckDuckGo Lite URL (HTML Version)
    url = "https://html.duckduckgo.com/html/"
    
    payload = {'q': query}
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://html.duckduckgo.com/"
    }

    try:
        # POST request bhej rahe hain taake query secure rahe
        resp = requests.post(url, data=payload, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []

        # 🕵️ HTML Parsing (DDG Lite Structure)
        # Har result 'div.result' mein hota hai
        for result in soup.select('.result'):
            title_tag = result.select_one('.result__title a')
            snippet_tag = result.select_one('.result__snippet')
            url_tag = result.select_one('.result__url')

            if title_tag and url_tag:
                link = title_tag['href']
                
                # Kabhi kabhi link relative hota hai, usay fix karna
                if link.startswith('//'):
                    link = 'https:' + link
                
                # Ad/Sponsor links ko ignore karna
                if "yandex" in link or "ad_provider" in link:
                    continue

                results.append({
                    "title": title_tag.get_text(strip=True),
                    "link": link,
                    "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "No description."
                })

        # Agar results khali hon (jo ke mushkil hai)
        if not results:
            return jsonify({
                "status": True, 
                "total_results": 0, 
                "msg": "No results found (Server might be busy)."
            })

        return jsonify({
            "status": True,
            "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐒𝐄𝐀𝐑𝐂𝐇",
            "source": "DuckDuckGo Lite",
            "total_results": len(results),
            "results": results[:10] # Top 10 results
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
  
