import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# 🛡️ Browser Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36"
]

# 1. SEARCH FUNCTION (English Data)
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
                # Sirf pehli 2 lines uthao taake jawab lamba na ho
                text = snippet.get_text(strip=True)
                return text[:300] # Max 300 characters
        return None
    except:
        return None

# 2. GOOGLE ROMANIZER (The Secret Hack)
def get_roman_urdu(text):
    try:
        # Hum 'hi' (Hindi) use kar rahe hain kyunke Google uski Romanization deta hai
        # Bolne mein Hindi/Urdu same hain.
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "hi",    # Target Hindi (Roman ke liye)
            "dt": ["t", "rm"], # 't'=Translation, 'rm'=Romanization
            "q": text
        }
        
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        resp = requests.get(base_url, params=params, headers=headers, timeout=5)
        data = resp.json()
        
        # Google JSON Structure: data[0] mein translation hoti hai
        # data[0] ka last element aksar Romanization hota hai
        
        if data and data[0]:
            # Akri element check karte hain jo string ho
            last_item = data[0][-1]
            if isinstance(last_item, list):
                # Kabhi kabhi array ke last index pe roman text hota hai
                return last_item[-1] 
            elif isinstance(last_item, str):
                return last_item
            
            # Fallback: Agar upar wala fail ho, to loop chalao
            roman_text = ""
            for item in data[0]:
                if len(item) >= 4 and item[3]: # Index 3 par aksar Roman hota hai
                    roman_text += item[3] + " "
            return roman_text.strip()
            
        return "Translation Error"
    except Exception as e:
        return str(e)

# 🌐 API ROUTE
@app.route('/api/roman-google', methods=['GET'])
def roman_google():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    # Step 1: Search (English)
    english_answer = get_search_result(query)
    
    if not english_answer:
        return jsonify({"status": False, "msg": "Jawab nahi mila."})

    # Step 2: Convert to Roman Urdu
    roman_answer = get_roman_urdu(english_answer)

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Google Roman)",
        "english": english_answer,
        "roman_urdu": roman_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
