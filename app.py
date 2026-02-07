import os
import requests
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 UNLIMITED KEYS POOL
# Jitni marzi keys yahan add karein
KEYS = [
    "AIzaSyB-oKyz7BlIz2k97d2Ln1PmV_o5U3fWrKk",
    "AIzaSyC-gp50_CveVGdoYANVvWXUsk6lFn9Ggec",
    "AIzaSyC0_syf_nF2-YHkfbK3oaSc20CxNp3skSU",
    "AIzaSyBhCiVOyjt3C7u8BwPUTrVYgEf1_l_T1Os",
    "AIzaSyCPOiw3O7rijjI6v0F3brfHod7jDXI39JU"
    # "AIzaSy..." (Aur keys bhi add kar sakte hain)
]

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈 - Unlimited Multi-Key Engine Active!"

@app.route('/api/search', methods=['GET'])
def ai_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Sawal missing hai!"})

    # 🔄 AUTO-RETRY LOGIC: Aik key fail ho toh dusri try karo
    random.shuffle(KEYS) # Keys ko mix kar dena taake load barabar rahe
    
    for key in KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
        headers = {'Content-Type': 'application/json'}
        
        # 🧠 Fixed Payload (v1beta Official Standard)
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Current Time: February 7, 2026. Search the web and answer accurately: {query}"
                }]
            }],
            "tools": [{
                "google_search_retrieval": {
                    "dynamic_retrieval_config": {
                        "mode": "MODE_DYNAMIC", # 👈 Fixed: "DYNAMIC" se "MODE_DYNAMIC" kar diya
                        "dynamic_threshold": 0.3
                    }
                }
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            res_data = response.json()

            # Agar response mein answer hai toh return karo
            if "candidates" in res_data:
                answer = res_data['candidates'][0]['content']['parts'][0]['text']
                return jsonify({
                    "status": True,
                    "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈",
                    "answer": answer
                })
            
            # Agar key limit hit hui hai, toh loop jari rakho (Next key check karo)
            print(f"Key {key[:10]}... failed, trying next key.")
            continue

        except Exception as e:
            print(f"Error with key: {str(e)}")
            continue

    # Agar saari keys fail ho jayein
    return jsonify({
        "status": False, 
        "error": "Saari keys ki limit khatam ho chuki hai. Nayi keys add karein!"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
