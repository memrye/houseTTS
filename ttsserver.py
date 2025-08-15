from flask import Flask, request
from gtts import gTTS
import os
import tempfile
import subprocess

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    if not text:
        return {"error": "No text provided"}, 400

    # Generate TTS audio file
    tmp_path = tempfile.mktemp(suffix=".mp3")
    tts = gTTS(text)
    tts.save(tmp_path)

    # Play audio through default system output (Bluetooth speaker)
    subprocess.run(["mpg123", tmp_path])  # mpg123 can play MP3s

    os.remove(tmp_path)
    return {"status": "played"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
