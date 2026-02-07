import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 API Key (Replit Secrets se ya direct)
API_KEY = "AIzaSyC9QQ9974G-0rkRz-_umswrgWx1ZztvIiU"
genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈 - Google Engine Fixed!"

@app.route('/api/search', methods=['GET'])
def ai_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Ustad ji, sawal toh bhejain!"})

    try:
        # 🧠 Fixed Tool Declaration
        # 'google_search_retrieval' asli field name hai
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{"google_search_retrieval": {}}] 
        )

        # AI Response Generation
        # Context 2026 set kiya gaya hai
        prompt = f"Current Date is February 7, 2026. Use Google Search to provide a detailed and 100% accurate answer for: {query}"
        response = model.generate_content(prompt)

        return jsonify({
            "status": True,
            "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐀𝐈",
            "answer": response.text
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
