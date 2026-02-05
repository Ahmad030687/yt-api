from flask import Flask, request, jsonify
import yt_dlp

# 1. Sabse pehle Flask engine start (Is se error nahi aayega)
app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX YouTube Search API is ONLINE."

# ---------------------------------------------------------
# 🎥 YOUTUBE SEARCH ROUTE (Standalone)
# ---------------------------------------------------------
@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: 
        return jsonify({"status": False, "msg": "Search query is required!"})

    try:
        # Ahmad Bhai: Ye search logic boht fast hai
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'default_search': 'ytsearch5', 
            'nocheckcertificate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
            video_list = []
            for entry in info.get('entries', []):
                video_list.append({
                    "title": entry.get('title'),
                    "id": entry.get('id'),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration": entry.get('duration_string'),
                    "views": f"{entry.get('view_count', 0):,}",
                    "thumbnail": entry.get('thumbnails')[-1]['url'] if entry.get('thumbnails') else None
                })

            return jsonify({
                "status": True,
                "query": query,
                "total": len(video_list),
                "results": video_list
            })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# 2. Render port configuration
if __name__ == '__main__':
    # Render hamesha port 10000 prefer karta hai
    app.run(host='0.0.0.0', port=10000)
    
