import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Import banned words list
bannedWords = os.getenv("BANNED_WORDS")
bannedList = bannedWords.split(",") if bannedWords else []

# Load URL and token
TOKEN = os.getenv("DISCORD_TOKEN")
TTS_SERVER_URL = "http://127.0.0.1:5000/tts"

# Initialise Discord Bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Create user dictionary and imports admin list
userData = {}  # stores {username: chosen_name}
admins = os.getenv("ADMIN_LIST")
adminList = admins.split(",") if admins else []

# Constants
maxMsgRepeatLength = 90
maxMsgLength = 150  
volumeDefault = 80

def returnUsername(username):
    return userData.get(username, username)

# Converts all strings to lower case and checks for banned words
def checkForBannedWords(discordMessage):
    return any(word.lower() in discordMessage.lower() for word in bannedList)

# Update nickname
async def renameCommand(message):
    content = message.content[3:].strip()
    author = str(message.author.name)
    userData[author] = content  # save nickname
    return await message.channel.send(f"I'll call you {content} now")

# Change volume 
async def volumeCommand(message):
    # Block non-admin users from changing volume
    if str(message.author.name) not in adminList:
        return await message.channel.send("Oh no no girl")

    # Get the new volume
    content = message.content[3:].strip()

    # If not a number cancel
    if not content.isnumeric():
        return await message.channel.send("Volume must be a number between 0 and 100")
    else:
        if 0 <= int(content) <= 100:
            volumeDefault = int(content)  # Store as percentage (0-100)
            # Send test volume to TTS server (convert to 0.0-1.0 scale)
            requests.post(TTS_SERVER_URL, json={"volume": volumeDefault / 100})
            return await message.channel.send(f"Volume set to {content}%")
        else:
            return await message.channel.send("Volume must be a number between 0 and 100")

# Checks if the message is too long and if not whether to repeat
async def textCheck(message, author, discordMessage):
    if len(discordMessage) > maxMsgLength:
        # Blocks the message for being too long
        await message.channel.send(f"Try me bitch, keep it shorter than {maxMsgLength} characters")
        return None
    if len(discordMessage) > maxMsgRepeatLength:
        # Play the message once
        return f"{author} says {discordMessage}"
    else:
        # Repeat the message a second time
        return f"{author} says {discordMessage} {discordMessage}"

async def speakCommand(message):
    # Get author and message
    author = returnUsername(str(message.author.name))
    discordMessage = message.content[3:].strip()
        
    if checkForBannedWords(discordMessage):
        return await message.channel.send("Chile stop it...")

    # Run text checks
    text = await textCheck(message, author, discordMessage)
    if not text:
        return

    # Send to TTS server WITH volume (convert to 0.0-1.0 scale)
    requests.post(TTS_SERVER_URL, json={"text": text, "volume": volumeDefault / 100})
    await message.channel.send(f"{text}")

@client.event
async def on_message(message):
    global volumeDefault  # Add this to modify the global variable
    
    # Ignore messages from the bot
    if message.author == client.user:
        return
    
    # Volume Command
    if message.content.startswith("!v "):
        await volumeCommand(message)

    # Rename Command
    if message.content.startswith("!r "):
        await renameCommand(message)
    
    # Speak Command
    if message.content.startswith("!s "):
        await speakCommand(message)

client.run(TOKEN)
