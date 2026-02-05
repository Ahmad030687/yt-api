from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX YouTube Search & Download API is ONLINE."

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

# --- UPDATED DOWNLOAD ROUTE ---
@app.route('/yt-dl')
def yt_dl():
    url = request.args.get('url')
    media_type = request.args.get('type', 'audio')
    
    if not url: return jsonify({"status": False, "msg": "URL missing"})

    try:
        # Ahmad Bhai: Is mein maine specific headers daal diye hain
        ydl_opts = {
            'format': 'bestaudio/best' if media_type == 'audio' else 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": info.get('url')
            })
    except Exception as e:
        # Ahmad bhai, yahan error log hoga toh aapko Render dashboard mein dikh jayega
        print(f"Error extracting: {str(e)}")
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
