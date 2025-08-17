import discord
import requests

TOKEN = "REPLACE-ME"
TTS_SERVER_URL = "http://127.0.0.1:5000/tts"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

sterling = "poundsterl1ng"
maeve = "maeveve"
gee = "gee6033"

space = ". "

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!s "):
        if str(message.author) == maeve:
            text = "maeve says " + message.content[3:] + space + message.content[3:]

        elif str(message.author) == sterling:
            text = "sterling says " + message.content[3:] + space + message.content[3:]

        elif str(message.author) == gee:
            text = "gee says " + message.content[3:] + space + message.content[3:]

        else:
            text = str(message.author) + " says " + message.content[3:] + space + message.content[3:]
        
        requests.post(TTS_SERVER_URL, json={"text": text})
        await message.channel.send(f"Speaking: {text}")

client.run(TOKEN)
