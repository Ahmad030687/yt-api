from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX YouTube Search & Download API is ONLINE."

# --- 1. SEARCH ROUTE ---
@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "msg": "Query missing"})
    try:
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
            results = []
            for entry in info.get('entries', []):
                results.append({
                    "title": entry.get('title'),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "thumbnail": entry.get('thumbnails')[-1]['url'] if entry.get('thumbnails') else None,
                    "views": f"{entry.get('view_count', 0):,}"
                })
            return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# --- 2. DOWNLOAD ROUTE (Ye 404 theek karega) ---
@app.route('/yt-dl')
def yt_dl():
    url = request.args.get('url')
    media_type = request.args.get('type', 'audio') # audio ya video
    
    if not url: return jsonify({"status": False, "msg": "URL missing"})

    try:
        # Ahmad Bhai: Ye direct mp3/mp4 link nikalne ki logic hai
        ydl_opts = {
            'format': 'bestaudio/best' if media_type == 'audio' else 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": info.get('url') # Direct stream link
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
