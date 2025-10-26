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

def load_cogs():
    # Logs
    bot.load_extension("cogs.logs.message_logs")
    bot.load_extension("cogs.logs.moderation_logs")
    bot.load_extension("cogs.logs.vocal_logs")
    bot.load_extension("cogs.logs.giveaway_logs")
    bot.load_extension("cogs.logs.security_logs")
    bot.load_extension("cogs.logs.cyber_logs")
    
    # Modération
    bot.load_extension("cogs.moderation.mute")
    bot.load_extension("cogs.moderation.ban")
    bot.load_extension("cogs.moderation.warn")

if __name__ == "__main__":
    load_cogs()  # ← synchrone
    bot.run(TOKEN)  # ← asynchrone, géré par run()