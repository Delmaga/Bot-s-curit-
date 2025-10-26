# cogs/logs/moderation_logs.py
from discord.ext import commands
import discord
from utils.embeds import log_embed

class ModerationLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None

    @commands.command(name="logs_moderation", description="Définir le salon pour les logs de modération")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel):
        self.log_channel_id = salon.id
        await ctx.respond(f"✅ Salon de logs modération défini sur {salon.mention}", ephemeral=False)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "🆕 Salon créé",
                f"**Nom** : {channel.name}\n**Type** : {type(channel).__name__}"
            ))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "❌ Salon supprimé",
                f"**Nom** : {channel.name}\n**Type** : {type(channel).__name__}"
            ))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch and before.name != after.name:
            await ch.send(embed=log_embed(
                "✏️ Salon renommé",
                f"**Avant** : {before.name}\n**Après** : {after.name}"
            ))

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "➕ Rôle créé",
                f"**Nom** : {role.name}\n**Couleur** : {role.color}"
            ))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "➖ Rôle supprimé",
                f"**Nom** : {role.name}"
            ))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            # Rôles ajoutés/retirés
            if before.roles != after.roles:
                added = set(after.roles) - set(before.roles)
                removed = set(before.roles) - set(after.roles)
                desc = ""
                if added:
                    desc += f"**Rôles ajoutés** : {', '.join(r.mention for r in added)}\n"
                if removed:
                    desc += f"**Rôles retirés** : {', '.join(r.mention for r in removed)}\n"
                if desc:
                    await ch.send(embed=log_embed(
                        "🎭 Rôles modifiés",
                        f"**Membre** : {after.mention}\n{desc}"
                    ))
            # Pseudo changé
            if before.nick != after.nick:
                await ch.send(embed=log_embed(
                    "📛 Pseudo changé",
                    f"**Membre** : {after.mention}\n**Avant** : {before.nick or before.name}\n**Après** : {after.nick or after.name}"
                ))

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if ch:
            await ch.send(embed=log_embed(
                "🔨 Membre banni",
                f"**Utilisateur** : {user} (`{user.id}`)"
            ))

async def setup(bot):
    await bot.add_cog(ModerationLogs(bot))