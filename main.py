# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Vérifie le token IMMÉDIATEMENT
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ La variable DISCORD_TOKEN n'est pas définie !")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne.")
    await bot.change_presence(activity=discord.Game(name="Sécurité • !logs"))

async def load_cogs():
    for root, dirs, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                # Construire le chemin relatif sous forme de module
                rel_path = os.path.relpath(os.path.join(root, file), "./cogs")
                module_path = rel_path.replace(os.sep, ".").replace(".py", "")
                try:
                    await bot.load_extension(f"cogs.{module_path}")
                    print(f"✅ Chargé : cogs.{module_path}")
                except Exception as e:
                    print(f"❌ Erreur : cogs.{module_path} → {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_cogs())
    bot.run(TOKEN)