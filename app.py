import requests
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# 🛡️ Anti-Block Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

# ----------------------------------------------------
# 1. BING SEARCH ENGINE (Unstoppable Method)
# ----------------------------------------------------
def search_bing(query):
    try:
        # Bing ka secret rasta (Search suggestions/snippets)
        url = f"https://www.bing.com/AS/Suggestions?pt=S&mkt=en-us&qry={query}"
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        
        resp = requests.get(url, headers=headers, timeout=10)
        
        # Bing HTML se data nikalna
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Bing aksar 'sa_tm' ya 'sa_sh' classes mein data deta hai
        results = soup.find_all('div', class_='sa_tm')
        if not results:
            # Plan B: Wikipedia
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
            wiki_resp = requests.get(wiki_url, timeout=5)
            if wiki_resp.status_code == 200:
                return wiki_resp.json().get('extract')
        
        # Sab results ko jor kar ek paragraph bana dena
        combined_text = ""
        for res in results[:2]: # Top 2 results
            combined_text += res.get_text(strip=True) + " "
            
        return combined_text if combined_text else None
    except Exception as e:
        print(f"Bing Error: {e}")
        return None

# ----------------------------------------------------
# 2. GOOGLE TRANSLATE (English -> Urdu)
# ----------------------------------------------------
def google_translate(text, target_lang='ur'):
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx", "sl": "auto", "tl": target_lang, "dt": "t", "q": text
        }
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        resp = requests.get(base_url, params=params, headers=headers, timeout=5)
        data = resp.json()
        
        translated_text = ""
        if data and data[0]:
            for part in data[0]:
                if part[0]:
                    translated_text += part[0]
        return translated_text
    except:
        return text

# 🌐 MAIN API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "msg": "Query missing!"})

    # Bing se data lo
    english_answer = search_bing(query)
    
    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "Bing aur Wiki dono se data nahi mila."
        })

    # Translate to Urdu
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Bing Engine)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
