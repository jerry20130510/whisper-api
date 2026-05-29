from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Whisper API is running"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    return jsonify({
        "text": "測試成功"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
