from flask import Flask, request
from gtts import gTTS
import os
import tempfile
import subprocess
import logging
from datetime import datetime

app = Flask(__name__) 

# Setup logging to file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tts_debug.log'),
        logging.StreamHandler()  # Also print to console
    ]
)

announcer = os.path.join(os.path.dirname(__file__), "MessageReceived.mp3")

@app.route("/tts", methods=["POST"])
def tts():
    # Get text body
    text = request.json.get("text", "")

    # Get volume, default to 0.8
    newVolume = request.json.get("volume", "")
    volume = float(newVolume) if newVolume else 0.8
    
    if text:
        # Generate TTS audio file
        tmp_path = tempfile.mktemp(suffix=".mp3")
        try:
            tts = gTTS(text)
            tts.save(tmp_path)
            logging.debug(f"TTS audio saved to: {tmp_path}")

            playbackVolume = f"volume={volume}"

            subprocess.run([
                "ffplay", "-autoexit", "-nodisp", 
                "-af", playbackVolume, announcer
            ], check=True)

            logging.debug("Playing TTS audio...")
            subprocess.run([
                "ffplay", "-autoexit", "-nodisp", 
                "-af", playbackVolume, tmp_path
            ], check=True)
            
            volume = 0.8
            return {"status": "played"}, 200
            
        except subprocess.CalledProcessError as e:
            logging.error(f"FFplay error: {e}")
            return {"status": "error", "message": "Playback failed"}, 500
            
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return {"status": "error", "message": "Internal server error"}, 500
            
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception as e:
                logging.warning(f"Could not remove temp file: {e}")

    else:
        logging.warning("Empty text received in request")
        return {"status": "error", "message": "No text provided"}, 400

if __name__ == "__main__":
    logging.info("TTS Server starting...")
    app.run(host="0.0.0.0", port=5000)