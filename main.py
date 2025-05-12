from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def index():
    return "yt-dlp API aktif!"

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url parametresi gerekli"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forceurl": True,
        "format": "best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "url": info.get("url"),
                "thumbnail": info.get("thumbnail")
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
