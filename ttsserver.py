from flask import Flask, request
from gtts import gTTS
import os
import tempfile
import subprocess
from just_playback import Playback


app = Flask(__name__)

masterVolume = 0.8  

playback = Playback()

playback.set_volume(masterVolume)

#announcer = "/MessageReceived.mp3"

announcer = os.path.join(os.path.dirname(__file__), "MessageReceived.mp3")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    volume = request.json.get("volume", "")
    if volume:
        # Set volume for playback
        masterVolume = float(volume)
    
    if text:
        # Generate TTS audio file
        tmp_path = tempfile.mktemp(suffix=".mp3")
        tts = gTTS(text)
        tts.save(tmp_path)

        playback.load_file(announcer)
        playback.play()
        playback.set_volume(masterVolume)
        while playback.active:
            import time
            time.sleep(0.1)

        playback.load_file(tmp_path)
        playback.play()
        playback.set_volume(masterVolume)
        while playback.active:
            import time
            time.sleep(0.1)  

        os.remove(tmp_path)
        return {"status": "played"}, 200
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
