from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import tempfile
import os

app = Flask(__name__)

# faster-whisper 比 openai-whisper 省記憶體，Render 免費方案才跑得動
# base 模型約 145MB，適合 512MB 記憶體限制
model = WhisperModel("tiny", device="cpu", compute_type="int8")

@app.route("/")
def home():
    return "Whisper API is running"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    suffix = os.path.splitext(audio_file.filename)[1] or ".mp3"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        audio_file.save(tmp.name)
        temp_path = tmp.name

    try:
        segments, info = model.transcribe(temp_path, language="zh")
        text = "".join(segment.text for segment in segments)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
