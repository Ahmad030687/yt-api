from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>RDX Search Engine is Live on Render!</h1>"

@app.route('/api/search', methods=['GET'])
def search_api():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Sawal likho ustad!"}), 400

    try:
        results = []
        # DuckDuckGo se taaza tareen data uthana (No API Key)
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append({
                    "title": r['title'],
                    "link": r['href'],
                    "snippet": r['body']
                })

        # Agar results mil jayein
        if results:
            return jsonify({
                "status": "Success",
                "owner": "AHMAD RDX",
                "query": query,
                "data": results
            })
        else:
            return jsonify({"error": "Koi result nahi mila."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
