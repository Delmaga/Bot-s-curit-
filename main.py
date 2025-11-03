# main.py
import os
import discord
from discord.ext import commands
import asyncio

# Récupère le token depuis Railway (obligatoire)
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN non défini. Configure-le dans Railway.")

# Intents (nécessaires pour les logs + surveillance de bots)
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.presences = True  # Pour détecter bots online/offline

bot = commands.Bot(
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est en ligne sur {len(bot.guilds)} serveurs.")
    try:
        synced = await bot.sync_commands()
        print(f"🔁 {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"⚠️ Erreur de sync : {e}")

# Charger les cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📦 Cog chargé : {filename}")
            except Exception as e:
                print(f"❌ Erreur chargement {filename} : {e}")

async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())