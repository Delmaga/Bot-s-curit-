# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Intents nécessaires
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne.")
    await bot.change_presence(activity=discord.Game(name="Sécurité • /logs"))

# Charger tous les cogs
async def load_cogs():
    for root, dirs, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, file), "./cogs")
                cog_path = rel_path.replace(os.sep, ".")[:-3]
                try:
                    await bot.load_extension(f"cogs.{cog_path}")
                    print(f"✅ Chargé : cogs.{cog_path}")
                except Exception as e:
                    print(f"❌ Erreur chargement {cog_path}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_cogs())
    bot.run(os.getenv("DISCORD_TOKEN"))