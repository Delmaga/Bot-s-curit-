# cogs/logs/vocal_logs.py
from discord.ext import commands
import discord
from utils.embeds import log_embed

class VocalLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None

    @commands.slash_command(name="logs_vocal", description="Définir le salon pour les logs vocaux")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel):
        self.log_channel_id = salon.id
        await ctx.respond(f"✅ Salon de logs vocaux défini sur {salon.mention}", ephemeral=False)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        if before.channel is None and after.channel:
            await ch.send(embed=log_embed(
                "🔊 Connexion vocale",
                f"{member.mention} a rejoint **{after.channel.name}**"
            ))
        elif before.channel and after.channel is None:
            await ch.send(embed=log_embed(
                "🔇 Déconnexion vocale",
                f"{member.mention} a quitté **{before.channel.name}**"
            ))
        elif before.channel != after.channel:
            await ch.send(embed=log_embed(
                "🔀 Changement de salon vocal",
                f"{member.mention} : **{before.channel.name}** → **{after.channel.name}**"
            ))

def setup(bot):
    bot.add_cog(VocalLogs(bot))