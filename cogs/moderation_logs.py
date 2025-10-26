# cogs/moderation_logs.py
from discord.ext import commands
import discord
from utils.embeds import log_embed
import asyncio

class ModerationLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None

    @commands.slash_command(name="logs_moderation", description="Définir le salon pour les logs de modération")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel):
        self.log_channel_id = salon.id
        await ctx.respond(f"✅ Salon de logs modération défini sur {salon.mention}", ephemeral=False)

    async def get_auditor(self, guild, action):
        """Récupère l'utilisateur ayant effectué l'action via l'audit log."""
        try:
            async for entry in guild.audit_logs(limit=5, action=action):
                # Vérifie que l'entrée est récente (moins de 10 sec)
                if (discord.utils.utcnow() - entry.created_at).total_seconds() < 10:
                    return entry.user
        except:
            pass
        return None

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        auditor = await self.get_auditor(channel.guild, discord.AuditLogAction.channel_create)
        author = auditor.mention if auditor else "Inconnu"

        await ch.send(embed=log_embed(
            "🆕 Salon créé",
            f"**Créé par** : {author}\n"
            f"**Nom** : {channel.name}\n"
            f"**Type** : {type(channel).__name__}"
        ))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        auditor = await self.get_auditor(channel.guild, discord.AuditLogAction.channel_delete)
        author = auditor.mention if auditor else "Inconnu"

        await ch.send(embed=log_embed(
            "❌ Salon supprimé",
            f"**Supprimé par** : {author}\n"
            f"**Nom** : {channel.name}\n"
            f"**Type** : {type(channel).__name__}"
        ))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        # Seulement si le nom change
        if before.name != after.name:
            auditor = await self.get_auditor(after.guild, discord.AuditLogAction.channel_update)
            author = auditor.mention if auditor else "Inconnu"

            await ch.send(embed=log_embed(
                "✏️ Salon renommé",
                f"**Modifié par** : {author}\n"
                f"**Avant** : {before.name}\n"
                f"**Après** : {after.name}"
            ))

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        auditor = await self.get_auditor(role.guild, discord.AuditLogAction.role_create)
        author = auditor.mention if auditor else "Inconnu"

        await ch.send(embed=log_embed(
            "➕ Rôle créé",
            f"**Créé par** : {author}\n"
            f"**Nom** : {role.name}\n"
            f"**Couleur** : {role.color}"
        ))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        auditor = await self.get_auditor(role.guild, discord.AuditLogAction.role_delete)
        author = auditor.mention if auditor else "Inconnu"

        await ch.send(embed=log_embed(
            "➖ Rôle supprimé",
            f"**Supprimé par** : {author}\n"
            f"**Nom** : {role.name}"
        ))

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        if before.name != after.name or before.color != after.color:
            auditor = await self.get_auditor(after.guild, discord.AuditLogAction.role_update)
            author = auditor.mention if auditor else "Inconnu"

            changes = []
            if before.name != after.name:
                changes.append(f"**Nom** : {before.name} → {after.name}")
            if before.color != after.color:
                changes.append(f"**Couleur** : {before.color} → {after.color}")

            await ch.send(embed=log_embed(
                "🎨 Rôle modifié",
                f"**Modifié par** : {author}\n" + "\n".join(changes)
            ))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not self.log_channel_id:
            return
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        # Changement de pseudo
        if before.nick != after.nick:
            # L'audit log ne capture pas toujours le changement de pseudo par l'utilisateur lui-même
            # On suppose que c'est l'utilisateur sauf si un modérateur l'a forcé
            auditor = await self.get_auditor(after.guild, discord.AuditLogAction.member_update)
            author = auditor.mention if auditor else after.mention

            await ch.send(embed=log_embed(
                "📛 Pseudo changé",
                f"**Modifié par** : {author}\n"
                f"**Membre** : {after.mention}\n"
                f"**Avant** : {before.nick or before.name}\n"
                f"**Après** : {after.nick or after.name}"
            ))

        # Rôles ajoutés/retirés
        if before.roles != after.roles:
            added = set(after.roles) - set(before.roles)
            removed = set(before.roles) - set(after.roles)

            auditor = await self.get_auditor(after.guild, discord.AuditLogAction.member_role_update)
            author = auditor.mention if auditor else "Inconnu"

            desc = f"**Membre** : {after.mention}\n"
            if added:
                desc += f"**Rôles ajoutés** : {', '.join(r.mention for r in added)}\n"
            if removed:
                desc += f"**Rôles retirés** : {', '.join(r.mention for r in removed)}\n"

            await ch.send(embed=log_embed(
                "🎭 Rôles modifiés",
                f"**Modifié par** : {author}\n{desc}"
            ))

def setup(bot):
    bot.add_cog(ModerationLogs(bot))