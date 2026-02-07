import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 Replit Secrets se Key uthana (Security ke liye)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈 - Gemini Live Research Active!"

@app.route('/api/search', methods=['GET'])
def ai_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Sawal missing hai!"})

    try:
        # 🧠 Gemini 2.0 Flash / 1.5 Pro Model with LIVE SEARCH
        # Hum AI ko tool de rahe hain ke wo Google par search kare
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash', # Aap 2.0-flash-exp bhi use kar sakte hain
            tools=[{"google_search": {}}] 
        )

        # AI ko instruction: Direct Google se scan kar ke jawab do
        response = model.generate_content(f"You are Ahmad RDX's Global Research AI. Search the live web and provide a 100% accurate, real-time answer for: {query}")

        return jsonify({
            "status": True,
            "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈",
            "answer": response.text
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    # Replit automatically port set karta hai
    app.run(host='0.0.0.0', port=8080)
    
