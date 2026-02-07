import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import random
import os
import time

app = Flask(__name__)

# 🛡️ Real Browser Headers (Taake hum insaan lagen)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
]

# 1. DUCKDUCKGO HTML SEARCH (POST Method - Anti Block)
def get_ddg_search(query):
    url = "https://html.duckduckgo.com/html/"
    
    # 🕵️ Fake Form Submission
    payload = {'q': query}
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://html.duckduckgo.com/",
        "Origin": "https://html.duckduckgo.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        # POST request bhej rahe hain (Ye GET se zyada strong hai)
        resp = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # HTML se snippet nikalna
            snippets = []
            for result in soup.select('.result__snippet'):
                text = result.get_text(strip=True)
                if text:
                    snippets.append(text)
            
            # Agar result mil gaya to top 2 lines wapis karo
            if snippets:
                return " ".join(snippets[:2])
                
        return None
    except Exception as e:
        print(f"DDG Error: {e}")
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
        return f"Translation Error: {str(e)}"

# 🌐 API ROUTE
@app.route('/api/smart-urdu', methods=['GET'])
def smart_urdu():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"status": False, "msg": "Sawal missing hai!"})

    # Step 1: DuckDuckGo se English Data lo
    english_answer = get_ddg_search(query)
    
    # Agar pehli baar mein na mile to 1 second ruk kar dobara try karo
    if not english_answer:
        time.sleep(1)
        english_answer = get_ddg_search(query)

    if not english_answer:
        return jsonify({
            "status": False, 
            "msg": "DuckDuckGo busy hai. Thori der baad try karein."
        })

    # Step 2: Translate to Urdu (Nastaliq)
    urdu_answer = google_translate(english_answer, 'ur')

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (DuckDuckGo + Urdu)",
        "original": english_answer,
        "translated": urdu_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
