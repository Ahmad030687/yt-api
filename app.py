from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐒𝐄𝐀𝐑𝐂𝐇 𝐄𝐍𝐆𝐈𝐍𝐄 𝐋𝐈𝐕𝐄"

# 🌐 RDX GLOBAL SEARCH API
@app.route('/api/search', methods=['GET'])
def rdx_search():
    query = request.args.get('q')
    limit = int(request.args.get('limit', 10)) # Default 10 results

    if not query:
        return jsonify({"status": False, "msg": "Search query missing!"})

    try:
        results = []
        # DDGS library use kar ke data nikalna
        with DDGS() as ddgs:
            # 'text' method web search ke liye hota hai
            search_gen = ddgs.text(query, max_results=limit)
            
            for r in search_gen:
                results.append({
                    "title": r['title'],
                    "link": r['href'],
                    "snippet": r['body']
                })

        return jsonify({
            "status": True,
            "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐒𝐄𝐀𝐑𝐂𝐇",
            "query": query,
            "total_results": len(results),
            "results": results
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
