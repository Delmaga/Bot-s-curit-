# main.py
import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN manquant !")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne.")
    print(f"✅ Commandes détectées : {len(bot.application_commands)}")

# Chargement automatique des cogs
from pathlib import Path
for cog_file in Path("cogs").glob("*.py"):
    if cog_file.stem != "__init__":
        bot.load_extension(f"cogs.{cog_file.stem}")

bot.run(TOKEN)