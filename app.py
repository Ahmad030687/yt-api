import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import random
import urllib.parse
import os

app = Flask(__name__)

# 🛡️ Browser Headers (Taake hum block na hon)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36"
]

# 1. SEARCH FUNCTION (DuckDuckGo Lite - English Data)
def get_search_result(query):
    url = "https://html.duckduckgo.com/html/"
    payload = {'q': query}
    headers = {"User-Agent": random.choice(USER_AGENTS), "Referer": "https://html.duckduckgo.com/"}
    
    try:
        resp = requests.post(url, data=payload, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Top 2 results ka snippet utha lete hain taake data poora ho
        snippets = []
        for result in soup.select('.result'):
            txt = result.select_one('.result__snippet')
            if txt:
                snippets.append(txt.get_text(strip=True))
                if len(snippets) >= 2: break # Sirf top 2 results
        
        return " ".join(snippets) if snippets else None
    except:
        return None

# 2. TRANSLATION FUNCTION (Pollinations Text AI - Free)
def convert_to_roman(text, original_query):
    try:
        # 🧠 Prompt Engineering: Hum AI ko bata rahe hain ke kaise jawab dena hai
        prompt = (
            f"You are a helpful assistant talking to Ahmad RDX. "
            f"Context from internet: {text}. "
            f"User Question: {original_query}. "
            f"Instruction: Explain the answer in 'Roman Urdu' (Hindi/Urdu written in English). "
            f"Keep it short (max 3 lines). Direct answer. No English script."
        )
        
        # Pollinations Text API (Ye ChatGPT-4o ya OpenAI model use karta hai background mein)
        encoded_prompt = urllib.parse.quote(prompt)
        api_url = f"https://text.pollinations.ai/{encoded_prompt}"
        
        response = requests.get(api_url, timeout=15)
        return response.text
    except Exception as e:
        return "Sorry, translation fail ho gayi. " + str(e)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 - Roman Search Engine Active"

@app.route('/api/smart-roman', methods=['GET'])
def smart_roman():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    # Step 1: Search (English)
    raw_data = get_search_result(query)
    
    if not raw_data:
        # Agar search se kuch na mile to AI apne dimagh se jawab de
        raw_data = "No internet data, use your internal knowledge."

    # Step 2: Convert to Roman Urdu
    final_answer = convert_to_roman(raw_data, query)

    return jsonify({
        "status": True,
        "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Pollinations AI)",
        "answer": final_answer
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
