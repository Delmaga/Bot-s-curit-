import os
import discord
from dotenv import load_dotenv

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
    print(f"✅ Commandes slash enregistrées : {len(bot.application_commands)}")

async def load_cogs():
    # Logs
    await bot.load_extension("cogs.logs.message_logs")
    await bot.load_extension("cogs.logs.moderation_logs")
    await bot.load_extension("cogs.logs.vocal_logs")
    await bot.load_extension("cogs.logs.giveaway_logs")
    await bot.load_extension("cogs.logs.security_logs")
    await bot.load_extension("cogs.logs.cyber_logs")
    
    # Modération
    await bot.load_extension("cogs.moderation.mute")
    await bot.load_extension("cogs.moderation.ban")
    await bot.load_extension("cogs.moderation.warn")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_cogs())
    bot.run(TOKEN)