from discord.ext import commands
import discord
from utils.embeds import log_embed
import os

class GiveawayLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None
        self.gw_bot_id = int(os.getenv("GIVEAWAY_BOT_ID", 0))

    @commands.slash_command(name="logs_giveaway", description="Définir le salon pour les logs de giveaways")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel):
        self.log_channel_id = salon.id
        await ctx.respond(f"✅ Salon de logs giveaways défini sur {salon.mention}", ephemeral=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.log_channel_id or not self.gw_bot_id:
            return
        if message.author.id != self.gw_bot_id or not message.author.bot:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "🎁 Giveaway détecté",
                f"**Lancé par** : {message.interaction.user.mention if message.interaction else 'Inconnu'}\n"
                f"**Salon** : {message.channel.mention}\n"
                f"[Voir le giveaway]({message.jump_url})"
            ))

def setup(bot):
    bot.add_cog(GiveawayLogs(bot))