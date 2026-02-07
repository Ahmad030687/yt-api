import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import random
import os
import urllib.parse

app = Flask(__name__)

# 🛡️ Mobile Headers (Taake hum purana phone lagen)
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
]

# 1. DUCKDUCKGO LITE SEARCH (The Unblockable Method)
def get_ddg_lite(query):
    # Ye URL sab se important hai. 'lite' version block nahi hota.
    url = "https://lite.duckduckgo.com/lite/"
    
    payload = {'q': query}
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://lite.duckduckgo.com/",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        # Session use kar rahe hain taake cookies save hon
        session = requests.Session()
        resp = session.post(url, data=payload, headers=headers, timeout=10)
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Lite version mein data table mein hota hai
        # Hum pehla snippet dhoond rahe hain
        snippets = []
        
        # Table rows ko scan karo
        rows = soup.find_all('tr')
        for row in rows:
            # Result snippet class usually nahi hoti, raw text uthana parta hai
            text = row.get_text(strip=True)
            # Filter: Check karo ke ye result hai ya kachra
            if len(text) > 50 and "DuckDuckGo" not in text and "Privacy" not in text:
                snippets.append(text)
                if len(snippets) >= 1: break # Sirf pehla result chahiye
        
        if snippets:
            return snippets[0]
            
        return None

    except Exception as e:
        print(f"Lite Error: {e}")
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
        
        headers = {"User-Agent": "Mozilla/5.0"}
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

    # Step 1: DuckDuckGo LITE se English Data lo
    english_answer = get_ddg_lite(query)
    
    if not english_answer:
        # Fallback: Agar Lite bhi fail ho to seedha Wikipedia check kar lo
        try:
            wiki_resp = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}")
            if wiki_resp.status_code == 200:
                english_answer = wiki_resp.json().get('extract')
        except:
            pass

    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "Maaf karein, koi data nahi mila."
        })

    # Step 2: Urdu Translate
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (DDG Lite)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
