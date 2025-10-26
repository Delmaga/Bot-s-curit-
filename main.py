# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN non défini !")

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