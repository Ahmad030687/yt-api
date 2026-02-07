from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗 𝐏𝐘𝐓𝐇𝐎𝐍 - Server is Live & Fixed!"

@app.route('/ahmad-dl')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": False, "msg": "Link missing!"})

    # 🛡️ UPDATED SETTINGS: To bypass YouTube Bot Detection
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        # Ye headers YouTube ko dhoka dene ke liye hain
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'referer': 'https://www.youtube.com/',
        'nocheckcertificate': True,
        'geo_bypass': True,
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Metadata extract karna
            info = ydl.extract_info(url, download=False)
            direct_url = info.get('url')
            
            if direct_url:
                return jsonify({
                    "status": True,
                    "brand": "𝐒𝐀𝐑𝐃𝐀𝐑 𝐑𝐃𝐗",
                    "title": info.get('title', 'Unknown Music'),
                    "duration": info.get('duration'),
                    "thumbnail": info.get('thumbnail'),
                    "url": direct_url
                })
            return jsonify({"status": False, "msg": "YouTube restricted this link for bots."})
            
    except Exception as e:
        # Pura error bhej rahe hain taake bot mein nazar aaye kya masla hai
        return jsonify({"status": False, "error": str(e), "msg": "Sign-in check or IP Blocked by YouTube"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
