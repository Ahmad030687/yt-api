import requests
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# 🔑 RapidAPI Credentials (Jo aapne provide kiye)
RAPID_API_KEY = "6f52b7d6a4msh63cfa1e9ad2f0bbp1c46a5jsna5344b9fe618"
RAPID_API_HOST = "duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com"

# 1. RAPID-SEARCH FUNCTION
def search_rapid_ddg(query):
    url = "https://duckduckgo-duckduckgo-zero-click-info.p.rapidapi.com/"
    
    querystring = {
        "q": query,
        "no_html": "1",
        "no_redirect": "1",
        "skip_disambig": "1",
        "format": "json"
    }

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": RAPID_API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()
        
        # DuckDuckGo Zero Click Info 'AbstractText' mein jawab deta hai
        if data.get("AbstractText"):
            return data["AbstractText"]
        # Agar Abstract khali ho toh RelatedTopics se pehla snippet uthao
        elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
            return data["RelatedTopics"][0].get("Text")
            
        return None
    except Exception as e:
        print(f"RapidAPI Error: {e}")
        return None

# 2. GOOGLE TRANSLATE (English -> Urdu)
def google_translate(text, target_lang='ur'):
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx", "sl": "auto", "tl": target_lang, "dt": "t", "q": text
        }
        resp = requests.get(base_url, params=params, timeout=5)
        data = resp.json()
        
        translated_text = ""
        if data and data[0]:
            for part in data[0]:
                if part[0]:
                    translated_text += part[0]
        return translated_text
    except:
        return text

# 🌐 API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "msg": "Query missing!"})

    # Step 1: RapidAPI se data lo
    english_answer = search_rapid_ddg(query)
    
    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "RapidAPI ne is sawal ka jawab nahi diya. Kuch aur poochein."
        })

    # Step 2: Translate to Urdu
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (RapidAPI)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
