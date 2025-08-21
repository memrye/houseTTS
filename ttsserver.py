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
    print(f"[DEBUG] Requested volume: {volume} -> Using af_volume: {af_volume}")
    
    if text:
        # Generate TTS audio file
        tmp_path = tempfile.mktemp(suffix=".mp3")
        tts = gTTS(text)
        tts.save(tmp_path)

        announcer_cmd = [
            "ffplay", "-autoexit", "-nodisp",
            "-af", f"volume={af_volume}",
            announcer
        ]
        print(f"[DEBUG] Playing announcer with command: {announcer_cmd}")
        subprocess.run(announcer_cmd)
        
        subprocess.run([
            "ffplay", "-autoexit", "-nodisp",
            "-af", f"volume={af_volume}",
            tmp_path
        ])

        os.remove(tmp_path)
        return {"status": "played"}, 200
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
