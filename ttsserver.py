from flask import Flask, request
from gtts import gTTS
import os
import tempfile
import subprocess
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tts_debug.log'),
        logging.StreamHandler()
    ]
)

announcer = os.path.join(os.path.dirname(__file__), "MessageReceived.mp3")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "").strip()
    volume = float(request.json.get("volume", 0.8))

    if not text:
        logging.warning("Empty text received in request")
        return {"status": "error", "message": "No text provided"}, 400

    tmp_path = tempfile.mktemp(suffix=".mp3")
    try:
        # Generate TTS with gTTS
        tts = gTTS(text)
        tts.save(tmp_path)
        logging.debug(f"TTS audio saved to: {tmp_path}")

        playbackVolume = f"volume={volume}"

        # Play short notification sound first (optional)
        subprocess.Popen([
            "ffplay", "-autoexit", "-nodisp", "-loglevel", "quiet",
            "-af", playbackVolume, announcer
        ])

        # Then play the generated TTS
        subprocess.Popen([
            "ffplay", "-autoexit", "-nodisp", "-loglevel", "quiet",
            "-af", playbackVolume, tmp_path
        ])

        logging.info(f"TTS played for: {text}")
        return {"status": "played"}, 200

    except Exception as e:
        logging.error(f"TTS generation or playback error: {e}")
        return {"status": "error", "message": str(e)}, 500

    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                logging.debug("Temp file removed")
            except Exception as e:
                logging.warning(f"Could not remove temp file: {e}")


if __name__ == "__main__":
    logging.info("TTS Server starting...")
    app.run(host="0.0.0.0", port=5000)
