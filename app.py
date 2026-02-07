import requests
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# 🔑 Nayi Google Search API Credentials
RAPID_API_KEY = "6f52b7d6a4msh63cfa1e9ad2f0bbp1c46a5jsna5344b9fe618"
RAPID_API_HOST = "google-search116.p.rapidapi.com"

# 1. GOOGLE SEARCH FUNCTION (RapidAPI)
def search_google_rapid(query):
    url = "https://google-search116.p.rapidapi.com/search"
    querystring = {"q": query}
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": RAPID_API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        data = response.json()
        
        # Google Search API results 'results' array mein deti hai
        if data.get("results") and len(data["results"]) > 0:
            # Pehle 2-3 results ko combine karke summary banana
            snippets = [res.get("description", "") for res in data["results"][:2]]
            return " ".join(snippets)
            
        return None
    except Exception as e:
        print(f"Google API Error: {e}")
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

    # Step 1: Real Google Search se data lo
    english_answer = search_google_rapid(query)
    
    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "Google ne is sawal ka jawab nahi diya."
        })

    # Step 2: Translate to Urdu
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Google Engine)",
        "original": english_answer[:500], # First 500 chars for reference
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
