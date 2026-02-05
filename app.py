import yt_dlp
from flask import Flask, request, jsonify

# Agar aapne pehle define nahi kiya toh:
# app = Flask(__name__)

# ---------------------------------------------------------
# 🎥 YOUTUBE SEARCH ENGINE (Ahmad RDX Exclusive)
# ---------------------------------------------------------
@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: 
        return jsonify({"status": False, "msg": "Search query is required!"})

    try:
        # Ahmad Bhai, ye options video ko load kiye baghair data nikalte hain (Fast)
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'default_search': 'ytsearch5', # Pehli 5 videos dhoondega
            'nocheckcertificate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Metadata extract karna
            info = ydl.extract_info(query, download=False)
            
            video_list = []
            for entry in info['entries']:
                video_list.append({
                    "title": entry.get('title'),
                    "id": entry.get('id'),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration": entry.get('duration_string'),
                    "views": f"{entry.get('view_count', 0):,}",
                    "thumbnail": entry.get('thumbnails')[-1]['url'] if entry.get('thumbnails') else None,
                    "channel": entry.get('uploader')
                })

            return jsonify({
                "status": True,
                "query": query,
                "total_found": len(video_list),
                "results": video_list,
                "engine": "Ahmad-RDX-YT-v1"
            })

    except Exception as e:
        return jsonify({
            "status": False, 
            "error": str(e),
            "msg": "YouTube servers are acting tough!"
        })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000)
