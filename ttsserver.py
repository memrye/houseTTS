from flask import Flask, request
from gtts import gTTS
import os
import tempfile
import subprocess
from just_playback import Playback


app = Flask(__name__)

playback = Playback()
playback.set_volume(0.8)

#announcer = "/MessageReceived.mp3"

announcer = os.path.join(os.path.dirname(__file__), "MessageReceived.mp3")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    volume = request.json.get("volume", "")
    if volume:
        # Set volume for playback
        Playback.set_volume(float(volume))
    
    if text:
        # Generate TTS audio file
        tmp_path = tempfile.mktemp(suffix=".mp3")
        tts = gTTS(text)
        tts.save(tmp_path)

        playback.load_file(announcer)
        playback.play()
        while playback.active:
            import time
            time.sleep(0.1)

        playback.load_file(tmp_path)
        playback.play()
        while playback.active:
            import time
            time.sleep(0.1)       # returns a handle

        os.remove(tmp_path)
        return {"status": "played"}, 200
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
