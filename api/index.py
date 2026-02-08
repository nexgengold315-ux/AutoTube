from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# Ye line sabse zaroori hai, ye HopWeb ko ijazat degi
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/get_video_info', methods=['POST', 'OPTIONS'])
def get_info():
    # CORS pre-flight request handle karne ke liye
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'quality': f.get('format_note', 'N/A'),
                        'extension': f.get('ext'),
                        'url': f.get('url')
                    })
            
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration_string'),
                'links': formats[:3]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel ke liye ye zaroori hai
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run()
    
