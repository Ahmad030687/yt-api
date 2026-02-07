from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import requests
import random
import os

app = Flask(__name__)

# 🛡️ Browser Headers (Translation ke liye)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36"
]

# 1. SEARCH FUNCTION (Library Method - Anti Block)
def get_search_result(query):
    try:
        # DDGS library use kar rahe hain jo block nahi hoti
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                # 'body' mein main jawab hota hai
                return results[0]['body']
        return None
    except Exception as e:
        print(f"Search Error: {e}")
        return None

# 2. GOOGLE TRANSLATE FUNCTION (English -> Urdu)
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
        return f"Translation Error: {str(e)}"

# 🌐 API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    # Step 1: Search (English)
    english_answer = get_search_result(query)
    
    if not english_answer:
        # Fallback: Agar search fail ho to message
        return jsonify({
            "status": False, 
            "msg": "Search Engine Busy. Try again in 5 seconds."
        })

    # Step 2: Translate to Urdu
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (DDGS + Google)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
