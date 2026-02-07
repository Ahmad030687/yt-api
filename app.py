import requests
from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import wikipedia
import random
import os

app = Flask(__name__)

# 🛡️ Anti-Block Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
]

# ----------------------------------------------------
# 1. DUCKDUCKGO SEARCH (Primary)
# ----------------------------------------------------
def search_ddg(query):
    try:
        # Official Library use kar rahe hain
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results and 'body' in results[0]:
                print("✅ Source: DuckDuckGo")
                return results[0]['body']
    except Exception as e:
        print(f"⚠️ DDG Fail: {e}")
    return None

# ----------------------------------------------------
# 2. WIKIPEDIA SEARCH (Secondary - Backup)
# ----------------------------------------------------
def search_wiki(query):
    try:
        # Wikipedia kabhi block nahi hota
        # Hum English Wikipedia se summary uthayenge
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        resp = requests.get(wiki_url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if 'extract' in data:
                print("✅ Source: Wikipedia")
                return data['extract']
    except Exception as e:
        print(f"⚠️ Wiki Fail: {e}")
    return None

# ----------------------------------------------------
# 3. DUCKDUCKGO INSTANT ANSWER (Tertiary - Backup)
# ----------------------------------------------------
def search_ddg_api(query):
    try:
        # Ye official API hai jo bots ke liye hai (No Block)
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if 'AbstractText' in data and data['AbstractText']:
            print("✅ Source: DDG API")
            return data['AbstractText']
    except:
        pass
    return None

# ----------------------------------------------------
# 4. TRANSLATOR (English -> Urdu)
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
    except Exception as e:
        return f"Translation Error: {str(e)}"

# 🌐 MAIN API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "msg": "Query missing!"})

    # 🔥 ENGINE START: Ek ke baad ek try karo
    
    # 1. Try DuckDuckGo
    english_answer = search_ddg(query)
    
    # 2. Agar fail, Try Wikipedia
    if not english_answer:
        english_answer = search_wiki(query)
        
    # 3. Agar fail, Try DDG API
    if not english_answer:
        english_answer = search_ddg_api(query)

    # 4. Agar sab fail ho jayein
    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "Server busy hai, lekin humne koshish poori ki. Wiki/DDG ne data nahi diya."
        })

    # 5. Translate Result
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Multi-Engine)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
