import discord
import requests

TOKEN = "REPLACE-ME"
TTS_SERVER_URL = "http://127.0.0.1:5000/tts"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!say "):
        text = str(message.author) + " says " + message.content[5:] + message.content[5:]
        requests.post(TTS_SERVER_URL, json={"text": text})
        await message.channel.send(f"Speaking: {text}")

client.run(TOKEN)
