# cogs/logs/message_logs.py
from discord.ext import commands
import discord
from utils.embeds import log_embed

class MessageLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None

    @commands.command(name="logs_message", description="Définir le salon pour les logs de messages")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel):
        self.log_channel_id = salon.id
        await ctx.respond(f"✅ Salon de logs messages défini sur {salon.mention}", ephemeral=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.log_channel_id:
            return
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(embed=log_embed(
                "📝 Message envoyé",
                f"**Auteur** : {message.author.mention} (`{message.author.id}`)\n"
                f"**Salon** : {message.channel.mention}\n"
                f"**Contenu** : {message.content[:1000] or '*[Pièce jointe / Embed]*'}"
            ))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content or not self.log_channel_id:
            return
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(embed=log_embed(
                "✏️ Message modifié",
                f"**Auteur** : {before.author.mention}\n"
                f"**Salon** : {before.channel.mention}\n"
                f"**Avant** : {before.content[:500]}\n"
                f"**Après** : {after.content[:500]}"
            ))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not self.log_channel_id:
            return
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(embed=log_embed(
                "🗑️ Message supprimé",
                f"**Auteur** : {message.author.mention} (`{message.author.id}`)\n"
                f"**Salon** : {message.channel.mention}\n"
                f"**Contenu** : {message.content[:1000] or '*[Pièce jointe]*'}"
            ))

async def setup(bot):
    await bot.add_cog(MessageLogs(bot))