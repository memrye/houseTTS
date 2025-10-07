import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Import banned words list
bannedWords = os.getenv("BANNED_WORDS")
bannedList = [word.strip() for word in bannedWords.split(",")] if bannedWords else []

# Load URL and token
TOKEN = os.getenv("DISCORD_TOKEN")
TTS_SERVER_URL = "http://127.0.0.1:5000/tts"

# Create user dictionary and imports admin list
userData = {}  # stores {username: chosen_name}
admins = os.getenv("ADMIN_LIST")
adminList = admins.split(",") if admins else []

# Constants
maxMsgRepeatLength = 90
maxMsgLength = 150
volumeDefault = 80

# Initialise Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# /r Command — Rename Yourself
# ----------------------------
@bot.tree.command(
    name="r",
    description="Set a nickname for yourself (max 15 characters)."
)
@app_commands.describe(
    nickname="What you want me to call you (max 15 characters)."
)
async def rename(
    interaction: discord.Interaction,
    nickname: app_commands.Range[str, 1, 15]
):
    author = str(interaction.user.name)
    userData[author] = nickname.strip()
    await interaction.response.send_message(f"I'll call you {nickname} now.")


# ---------------------------------------
# /s Command — Speak Message with Optional Int
# ---------------------------------------
@bot.tree.command(
    name="s",
    description="Speak a message with an optional number (1–100)."
)
@app_commands.describe(
    text="The text you want me to say.",
    number="An optional integer between 1 and 100."
)
async def speak(
    interaction: discord.Interaction,
    text: str,
    number: app_commands.Range[int, 1, 100] | None = None
):
    author = interaction.user.name
    discordMessage = text.strip()

    if any(word.lower() in discordMessage.lower() for word in bannedList):
        await interaction.response.send_message("Chile stop it...")
        return

    if len(discordMessage) > maxMsgLength:
        await interaction.response.send_message(
            f"Try me bitch, keep it shorter than {maxMsgLength} characters"
        )
        return

    if len(discordMessage) > maxMsgRepeatLength:
        text_to_say = f"{author} says {discordMessage}"
    else:
        text_to_say = f"{author} says {discordMessage} {discordMessage}"

    
    payload = {
        "text": text_to_say,
        "volume": (number or volumeDefault) / 100
        }

    requests.post(TTS_SERVER_URL, json=payload)
    await interaction.response.send_message(f"{text_to_say}")


# ----------------------------
# Bot Ready Event
# ----------------------------

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("Slash commands synced and ready.")

# ----------------------------
# Run the Bot
# ----------------------------

bot.run(TOKEN)
