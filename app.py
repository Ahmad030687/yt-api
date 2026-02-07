import os
import requests
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 UNLIMITED KEYS LIST
# Yahan 5, 10 ya jitni marzi keys add karein
KEYS = [
    "AIzaSyB-oKyz7BlIz2k97d2Ln1PmV_o5U3fWrKk", # Key 1
    "AIzaSyC-gp50_CveVGdoYANVvWXUsk6lFn9Ggec",          # Key 2
    "AIzaSyC0_syf_nF2-YHkfbK3oaSc20CxNp3skSU",
    "AIzaSyBhCiVOyjt3C7u8BwPUTrVYgEf1_l_T1Os,
    "AIzaSyCPOiw3O7rijjI6v0F3brfHod7jDXI39JU"
]

@app.route('/')
def home():
    return f"🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈 - Unlimited Engine Active with {len(KEYS)} Keys!"

@app.route('/api/search', methods=['GET'])
def ai_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Sawal missing hai!"})

    # 🔄 Har bar random key uthana taake limit na aye
    selected_key = random.choice(KEYS)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={selected_key}"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Search the web and answer accurately for 2026: {query}"
            }]
        }],
        "tools": [{
            "google_search_retrieval": {
                "dynamic_retrieval_config": {
                    "mode": "DYNAMIC",
                    "dynamic_threshold": 0.3
                }
            }
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_data = response.json()

        if "candidates" in res_data:
            answer = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({
                "status": True,
                "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈",
                "key_used": f"Key_{KEYS.index(selected_key) + 1}", # Debugging ke liye
                "answer": answer
            })
        else:
            # Agar aik key fail ho toh error handle karna
            return jsonify({"status": False, "error": "This key hit its limit", "raw": res_data})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
