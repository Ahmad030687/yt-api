from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import requests
import random
import os
import time

app = Flask(__name__)

# 🛡️ Browser Headers (Translation ke liye)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/123.0.0.0 Safari/537.36"
]

# 1. DUCKDUCKGO OFFICIAL SEARCH
def get_ddg_result(query):
    try:
        # Official Library Initialize
        with DDGS() as ddgs:
            # Hum 'text' search use kar rahe hain jo sabse fast hai
            # max_results=1 taake pehla aur sabse best jawab mile
            results = list(ddgs.text(query, region='wt-wt', safesearch='off', max_results=1))
            
            if results:
                # 'body' mein main snippet hota hai
                return results[0]['body']
                
    except Exception as e:
        print(f"DDG Error: {e}")
        return None
    return None

# 2. GOOGLE TRANSLATE (English -> Urdu)
def google_translate(text, target_lang='ur'):
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto", 
            "tl": target_lang, # Urdu (ur)
            "dt": "t",
            "q": text
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
    except Exception as e:
        return f"Translation Error: {str(e)}"

# 🌐 API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"status": False, "msg": "Sawal missing hai!"})

    # Retry Logic: Agar pehli baar mein fail ho to 1 second baad dubara try karo
    english_answer = get_ddg_result(query)
    
    if not english_answer:
        time.sleep(1) # Thora saans lo
        english_answer = get_ddg_result(query)

    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "DuckDuckGo connect nahi ho saka. Dobara try karein."
        })

    # Translate
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Official DDG)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
