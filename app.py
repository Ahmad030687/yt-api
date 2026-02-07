import requests
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# 🛡️ Browser Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36"
]

# 1. WIKIPEDIA SEARCH (Ye Block Nahi Hota)
def get_wiki_data(query):
    try:
        # Wikipedia API (No Key Required)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        resp = requests.get(url, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            # Agar summary mil jaye
            if 'extract' in data:
                return data['extract']
        return None
    except:
        return None

# 2. GOOGLE TRANSLATE (English -> Urdu)
def google_translate(text, target_lang='ur'):
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto", 
            "tl": target_lang, # Urdu
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
        return str(e)

# 🌐 API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"status": False, "msg": "Sawal missing hai!"})

    # Step 1: Wikipedia se English Data lo
    english_answer = get_wiki_data(query)
    
    # Agar Wikipedia fail ho jaye (Fallback)
    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "Maloomat nahi mili. Spelling check karein."
        })

    # Step 2: Translate to Urdu
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Wiki + Urdu)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
