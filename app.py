from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐏𝐘𝐓𝐇𝐎𝐍 - Server is Live!"

@app.route('/ahmad-dl')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": False, "msg": "Link missing!"})

    # 🛠️ PRO SETTINGS: Faster extraction & Audio focus
    ydl_opts = {
        'format': 'bestaudio/best', # Sirf audio ka best link nikalna
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'force_generic_extractor': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info extract karna bina download kiye
            info = ydl.extract_info(url, download=False)
            
            # Direct Stream URL nikalna
            direct_url = info.get('url')
            
            if direct_url:
                return jsonify({
                    "status": True,
                    "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗",
                    "title": info.get('title', 'Unknown Music'),
                    "duration": info.get('duration'),
                    "thumbnail": info.get('thumbnail'),
                    "url": direct_url # Ye asli audio link hai
                })
            return jsonify({"status": False, "msg": "Could not extract direct link!"})
            
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
