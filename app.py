import yt_dlp
from flask import Flask, request, jsonify

# ... (baaki purana code)

# ---------------------------------------------------------
# 🎥 YOUTUBE SEARCH & INFO API (Ahmad RDX Build)
# ---------------------------------------------------------
@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "msg": "Search query missing"})

    try:
        # Search settings
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'default_search': 'ytsearch3' # Pehli 3 videos search karega
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = []
            
            for entry in info['entries']:
                results.append({
                    "title": entry.get('title'),
                    "id": entry.get('id'),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration": entry.get('duration_string'),
                    "views": entry.get('view_count'),
                    "thumbnail": entry.get('thumbnails')[-1]['url']
                })

            return jsonify({
                "status": True,
                "query": query,
                "results": results,
                "engine": "Ahmad-RDX-YT-v1"
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})
