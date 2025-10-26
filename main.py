# main.py
import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN manquant !")

# Bot avec intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne.")
    print(f"✅ Nombre de commandes : {len(bot.application_commands)}")

# NE CHARGE RIEN MANUELLEMENT → py-cord le fait automatiquement
# si les cogs sont dans un dossier nommé "cogs"

bot.run(TOKEN)