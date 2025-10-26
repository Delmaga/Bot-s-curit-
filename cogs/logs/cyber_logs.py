# cogs/logs/cyber_logs.py
from discord.ext import commands
import discord
from utils.embeds import log_embed

class CyberLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None

    @commands.command(name="logs_cyber", description="Définir le salon pour les logs cyber critiques")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel):
        self.log_channel_id = salon.id
        await ctx.respond(f"✅ Salon de logs cyber défini sur {salon.mention}", ephemeral=False)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            age = (discord.utils.utcnow() - member.created_at).days
            if age < 1:
                await ch.send(embed=log_embed(
                    "🚨 Nouveau compte (risque élevé)",
                    f"{member.mention} (`{member.id}`) vient de rejoindre.\n"
                    f"**Créé il y a** : {age} jour(s)\n"
                    f"**Membres totaux** : {member.guild.member_count}"
                ))

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "✉️ Invitation créée",
                f"**Créée par** : {invite.inviter.mention if invite.inviter else 'Inconnu'}\n"
                f"**Utilisations** : {invite.max_uses or 'Illimitées'}\n"
                f"**Expire dans** : {invite.max_age or 'Jamais'}s"
            ))

def setup(bot):
    bot.add_cog(CyberLogs(bot))