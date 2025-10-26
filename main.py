# main.py
import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN non défini !")

# Bot GLOBAL (pas de debug_guilds)
bot = discord.Bot(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne.")
    print(f"✅ En attente de synchronisation globale des commandes...")

# Charge les cogs normalement
async def load_cogs():
    for root, dirs, files in os.walk("./cogs"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel = os.path.relpath(os.path.join(root, file), "./cogs")
                mod = rel.replace(os.sep, ".").replace(".py", "")
                try:
                    await bot.load_extension(f"cogs.{mod}")
                    print(f"✅ Chargé : {mod}")
                except Exception as e:
                    print(f"❌ Erreur : {mod} → {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_cogs())
    bot.run(TOKEN)