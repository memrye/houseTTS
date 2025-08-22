import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TTS_SERVER_URL = "http://127.0.0.1:5000/tts"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

user_data = {}  # stores {username: chosen_name}

repeatMsgLen = 100
maxMsgLen = 200  # Discord's max message length
volumeDefault = 80  # This is 80% (0.8 when divided by 100)

@client.event
async def on_message(message):
    global volumeDefault  # Add this to modify the global variable
    
    # --- Ignore messages from the bot itself ---
    if message.author == client.user:
        return
    
    if message.content.startswith("!v "):
        content = message.content[3:].strip()
        if not content.isnumeric():
            return await message.channel.send("Volume must be a number between 0 and 100")
        else:
            if 0 <= int(content) <= 100:
                volumeDefault = int(content)  # Store as percentage (0-100)
                # Send test volume to TTS server (convert to 0.0-1.0 scale)
                requests.post(TTS_SERVER_URL, json={"volume": volumeDefault / 100})
                return await message.channel.send(f"Volume set to {content}%")

    # --- Register a nickname ---
    if message.content.startswith("!r "):
        content = message.content[3:].strip()
        username = str(message.author.name)
        user_data[username] = content  # save nickname
        await message.channel.send(f"I'll call you {content} now")
    
    if message.content.startswith("!s "):
        username = str(message.author.name)
        # Use registered nickname if exists, otherwise default to username
        display_name = user_data.get(username, username)

        text_body = message.content[3:].strip()
        if len(text_body) > maxMsgLen:
            return await message.channel.send(f"Try me bitch, I can only handle {maxMsgLen} characters at a time!")
        if len(text_body) > repeatMsgLen:
            text = f"{display_name} says {text_body}"
        else:
            text = f"{display_name} says {text_body} {text_body}"

        # Send to TTS server WITH volume (convert to 0.0-1.0 scale)
        requests.post(TTS_SERVER_URL, json={"text": text, "volume": volumeDefault / 100})
        await message.channel.send(f"Speaking: {text}")

client.run(TOKEN)