from flask import Flask, request
from gtts import gTTS
import os
import tempfile
import subprocess

app = Flask(__name__) 

#announcer = "/MessageReceived.mp3"

announcer = os.path.join(os.path.dirname(__file__), "MessageReceived.mp3")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    volume = request.json.get("volume", "")
    af_volume = float(volume) if volume else 0.8
    
    if text:
        # Generate TTS audio file
        tmp_path = tempfile.mktemp(suffix=".mp3")
        tts = gTTS(text)
        tts.save(tmp_path)

        # FFmpeg command
        subprocess.run([
            "ffplay", "-autoexit", "-nodisp",
            "-af", f"volume={af_volume}",
            announcer
        ])

        subprocess.run([
            "ffplay", "-autoexit", "-nodisp",
            "-af", f"volume={af_volume}",
            tmp_path
        ])

        os.remove(tmp_path)
        return {"status": "played"}, 200
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
