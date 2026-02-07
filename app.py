import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import random
import urllib.parse
import os

app = Flask(__name__)

# 🛡️ Browser Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36"
]

# 1. SEARCH FUNCTION (English Data layega)
def get_search_result(query):
    url = "https://html.duckduckgo.com/html/"
    payload = {'q': query}
    headers = {"User-Agent": random.choice(USER_AGENTS), "Referer": "https://html.duckduckgo.com/"}
    
    try:
        resp = requests.post(url, data=payload, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Top snippet uthao
        for result in soup.select('.result'):
            snippet = result.select_one('.result__snippet')
            if snippet:
                return snippet.get_text(strip=True)
        return None
    except:
        return None

# 2. GOOGLE TRANSLATE FUNCTION (Jo code aapne diya us se banaya hai)
def google_translate(text, target_lang='ur'):
    try:
        # Google GTX API URL
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",      # Source Language (Auto detect)
            "tl": target_lang, # Target Language (Urdu)
            "dt": "t",
            "q": text
        }
        
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        resp = requests.get(base_url, params=params, headers=headers, timeout=5)
        data = resp.json()
        
        # Response parsing (Loop through segments)
        translated_text = ""
        if data and data[0]:
            for part in data[0]:
                if part[0]:
                    translated_text += part[0]
                    
        return translated_text
    except Exception as e:
        return str(e)

# 🌐 API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    lang = request.args.get('lang', 'ur') # Default Urdu (ur)
    
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    # Step 1: Internet se English Answer lo
    english_answer = get_search_result(query)
    
    if not english_answer:
        return jsonify({"status": False, "msg": "Jawab nahi mila internet par."})

    # Step 2: Google se Translate karwao
    urdu_answer = google_translate(english_answer, lang)

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Google API)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
        
