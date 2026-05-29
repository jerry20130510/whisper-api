from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)

model = whisper.load_model("base")

@app.route("/")
def home():
return "Whisper API is running"

@app.route("/transcribe", methods=["POST"])
def transcribe():
if "file" not in request.files:
return jsonify({"error": "No file uploaded"}), 400

```
audio_file = request.files["file"]
suffix = os.path.splitext(audio_file.filename)[1] or ".mp3"

with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
    audio_file.save(tmp.name)
    temp_path = tmp.name

try:
    result = model.transcribe(temp_path, language="zh")
    return jsonify({"text": result["text"]})
except Exception as e:
    return jsonify({"error": str(e)}), 500
finally:
    if os.path.exists(temp_path):
        os.remove(temp_path)
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=10000)
