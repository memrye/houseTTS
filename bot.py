import discord
import requests

TOKEN = "REPLACE-ME"
TTS_SERVER_URL = "http://127.0.0.1:5000/tts"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

user_data = {}  # stores {username: chosen_name}

space = ". "

@client.event
async def on_message(message):
    # --- Ignore messages from the bot itself ---
    if message.author == client.user:
        return

    # --- Register a nickname ---
    if message.content.startswith("!r "):
        content = message.content[3:].strip()
        username = str(message.author.name)
        user_data[username] = content  # save nickname
        await message.channel.send(f"{username}, I'll call you {content} now!")
    
    if message.content.startswith("!s "):
        username = str(message.author.name)
        # Use registered nickname if exists, otherwise default to username
        display_name = user_data.get(username, username)

        text_body = message.content[3:].strip()
        text = f"{display_name} says {text_body} {text_body}"

        # Send to TTS server
        requests.post(TTS_SERVER_URL, json={"text": text})
        await message.channel.send(f"Speaking: {text}")

client.run(TOKEN)
