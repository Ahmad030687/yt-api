from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 - AI Chat Engine Active"

@app.route('/api/smart-roman', methods=['GET'])
def smart_roman():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "msg": "Query missing!"})

    try:
        # 🦅 DuckDuckGo AI (GPT-4o Mini Model - Free)
        # Ye search bhi karega aur translate bhi
        with DDGS() as ddgs:
            
            # Hum AI ko strict instruction de rahe hain
            prompt = (
                f"User Question: {query}\n"
                f"Instruction: Search the internet or use your knowledge to answer this question. "
                f"Answer ONLY in 'Roman Urdu' (Hindi/Urdu written in English). "
                f"Keep it short (max 2-3 lines). Be accurate."
            )

            # 'gpt-4o-mini' model use kar rahe hain jo fast hai
            response = ddgs.chat(prompt, model='gpt-4o-mini')

            # Agar response mil jaye
            if response:
                return jsonify({
                    "status": True,
                    "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (DDG AI)",
                    "answer": response
                })
            else:
                return jsonify({"status": False, "msg": "AI ne jawab nahi diya."})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
