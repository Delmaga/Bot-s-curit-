# cogs/comprehensive_logs.py
from discord.ext import commands
import discord
from utils.embeds import log_embed
import asyncio

class ComprehensiveLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = {
            "message": None,
            "vocal": None,
            "role": None,
            "salon": None,
            "categorie": None,
            "spam": None,
            "pseudo": None,
            "ban": None,
            "mute": None,
            "warn": None,
            "moov": None,
        }

    def get_channel(self, name):
        return self.bot.get_channel(self.channels.get(name))

    # === Commandes pour définir les salons de logs ===
    @commands.slash_command(name="logs_message", description="Salon pour logs messages")
    @commands.has_permissions(administrator=True)
    async def set_msg_log(self, ctx, salon: discord.TextChannel):
        self.channels["message"] = salon.id
        await ctx.respond(f"✅ Logs messages → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_vocal", description="Salon pour logs vocaux")
    @commands.has_permissions(administrator=True)
    async def set_voc_log(self, ctx, salon: discord.TextChannel):
        self.channels["vocal"] = salon.id
        await ctx.respond(f"✅ Logs vocaux → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_role", description="Salon pour logs rôles")
    @commands.has_permissions(administrator=True)
    async def set_role_log(self, ctx, salon: discord.TextChannel):
        self.channels["role"] = salon.id
        await ctx.respond(f"✅ Logs rôles → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_salon", description="Salon pour logs salons")
    @commands.has_permissions(administrator=True)
    async def set_salon_log(self, ctx, salon: discord.TextChannel):
        self.channels["salon"] = salon.id
        await ctx.respond(f"✅ Logs salons → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_categorie", description="Salon pour logs catégories")
    @commands.has_permissions(administrator=True)
    async def set_cat_log(self, ctx, salon: discord.TextChannel):
        self.channels["categorie"] = salon.id
        await ctx.respond(f"✅ Logs catégories → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_spam", description="Salon pour logs spam")
    @commands.has_permissions(administrator=True)
    async def set_spam_log(self, ctx, salon: discord.TextChannel):
        self.channels["spam"] = salon.id
        await ctx.respond(f"✅ Logs spam → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_pseudo", description="Salon pour logs pseudos")
    @commands.has_permissions(administrator=True)
    async def set_nick_log(self, ctx, salon: discord.TextChannel):
        self.channels["pseudo"] = salon.id
        await ctx.respond(f"✅ Logs pseudos → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_ban", description="Salon pour logs bans")
    @commands.has_permissions(administrator=True)
    async def set_ban_log(self, ctx, salon: discord.TextChannel):
        self.channels["ban"] = salon.id
        await ctx.respond(f"✅ Logs bans → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_mute", description="Salon pour logs mutes")
    @commands.has_permissions(administrator=True)
    async def set_mute_log(self, ctx, salon: discord.TextChannel):
        self.channels["mute"] = salon.id
        await ctx.respond(f"✅ Logs mutes → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_warn", description="Salon pour logs warns")
    @commands.has_permissions(administrator=True)
    async def set_warn_log(self, ctx, salon: discord.TextChannel):
        self.channels["warn"] = salon.id
        await ctx.respond(f"✅ Logs warns → {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_moov", description="Salon pour logs déplacements vocaux")
    @commands.has_permissions(administrator=True)
    async def set_moov_log(self, ctx, salon: discord.TextChannel):
        self.channels["moov"] = salon.id
        await ctx.respond(f"✅ Logs déplacements → {salon.mention}", ephemeral=False)

    # === Utilitaire : récupérer l'auteur via audit log ===
    async def get_auditor(self, guild, action, target=None):
        try:
            async for entry in guild.audit_logs(limit=5, action=action):
                if (discord.utils.utcnow() - entry.created_at).total_seconds() < 10:
                    if target is None or entry.target.id == target.id:
                        return entry.user
        except:
            pass
        return None

    # === Logs messages ===
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.channels["message"]:
            return
        ch = self.get_channel("message")
        if ch:
            await ch.send(embed=log_embed(
                "📝 Message envoyé",
                f"**Auteur** : {message.author.mention}\n"
                f"**Contenu** : {message.content[:1000] or '*[Pièce jointe]*'}"
            ))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content or not self.channels["message"]:
            return
        ch = self.get_channel("message")
        if ch:
            await ch.send(embed=log_embed(
                "✏️ Message modifié",
                f"**Auteur** : {before.author.mention}\n"
                f"**Avant** : {before.content[:500]}\n"
                f"**Après** : {after.content[:500]}"
            ))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not self.channels["message"]:
            return
        ch = self.get_channel("message")
        if ch:
            await ch.send(embed=log_embed(
                "🗑️ Message supprimé",
                f"**Auteur** : {message.author.mention}\n"
                f"**Contenu** : {message.content[:1000] or '*[Pièce jointe]*'}"
            ))

    # === Logs vocaux ===
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not any((self.channels["vocal"], self.channels["moov"])):
            return

        # Connexion/déconnexion
        if before.channel is None and after.channel:
            ch = self.get_channel("vocal")
            if ch:
                await ch.send(embed=log_embed(
                    "🔊 Connexion vocale",
                    f"{member.mention} a rejoint {after.channel.mention}"
                ))
        elif before.channel and after.channel is None:
            ch = self.get_channel("vocal")
            if ch:
                await ch.send(embed=log_embed(
                    "🔇 Déconnexion vocale",
                    f"{member.mention} a quitté {before.channel.mention}"
                ))

        # Déplacement
        if before.channel and after.channel and before.channel != after.channel:
            ch = self.get_channel("moov")
            if ch:
                await ch.send(embed=log_embed(
                    "🔀 Déplacement vocal",
                    f"{member.mention} : {before.channel.mention} → {after.channel.mention}"
                ))

    # === Logs rôles ===
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if not self.channels["role"]:
            return
        auditor = await self.get_auditor(role.guild, discord.AuditLogAction.role_create, role)
        ch = self.get_channel("role")
        if ch:
            await ch.send(embed=log_embed(
                "➕ Rôle créé",
                f"**Créé par** : {auditor.mention if auditor else 'Inconnu'}\n"
                f"**Nom** : {role.name}\n"
                f"**Couleur** : {role.color}\n"
                f"**Permissions** : {role.permissions.value}"
            ))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if not self.channels["role"]:
            return
        auditor = await self.get_auditor(role.guild, discord.AuditLogAction.role_delete, role)
        ch = self.get_channel("role")
        if ch:
            await ch.send(embed=log_embed(
                "➖ Rôle supprimé",
                f"**Supprimé par** : {auditor.mention if auditor else 'Inconnu'}\n"
                f"**Nom** : {role.name}"
            ))

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if not self.channels["role"]:
            return
        changes = []
        if before.name != after.name:
            changes.append(f"**Nom** : {before.name} → {after.name}")
        if before.color != after.color:
            changes.append(f"**Couleur** : {before.color} → {after.color}")
        if before.permissions != after.permissions:
            changes.append(f"**Permissions** : modifiées")

        if changes:
            auditor = await self.get_auditor(after.guild, discord.AuditLogAction.role_update, after)
            ch = self.get_channel("role")
            if ch:
                await ch.send(embed=log_embed(
                    "🎨 Rôle modifié",
                    f"**Modifié par** : {auditor.mention if auditor else 'Inconnu'}\n" + "\n".join(changes)
                ))

    # === Logs salons & catégories ===
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        ch_type = "categorie" if isinstance(channel, discord.CategoryChannel) else "salon"
        if not self.channels[ch_type]:
            return
        auditor = await self.get_auditor(channel.guild, discord.AuditLogAction.channel_create, channel)
        log_ch = self.get_channel(ch_type)
        if log_ch:
            await log_ch.send(embed=log_embed(
                f"🆕 {'Catégorie' if ch_type == 'categorie' else 'Salon'} créé",
                f"**Créé par** : {auditor.mention if auditor else 'Inconnu'}\n"
                f"**Nom** : {channel.name}"
            ))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        ch_type = "categorie" if isinstance(channel, discord.CategoryChannel) else "salon"
        if not self.channels[ch_type]:
            return
        auditor = await self.get_auditor(channel.guild, discord.AuditLogAction.channel_delete, channel)
        log_ch = self.get_channel(ch_type)
        if log_ch:
            await log_ch.send(embed=log_embed(
                f"❌ {'Catégorie' if ch_type == 'categorie' else 'Salon'} supprimée",
                f"**Supprimé par** : {auditor.mention if auditor else 'Inconnu'}\n"
                f"**Nom** : {channel.name}"
            ))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name == after.name:
            return
        ch_type = "categorie" if isinstance(after, discord.CategoryChannel) else "salon"
        if not self.channels[ch_type]:
            return
        auditor = await self.get_auditor(after.guild, discord.AuditLogAction.channel_update, after)
        log_ch = self.get_channel(ch_type)
        if log_ch:
            await log_ch.send(embed=log_embed(
                f"✏️ {'Catégorie' if ch_type == 'categorie' else 'Salon'} renommée",
                f"**Modifié par** : {auditor.mention if auditor else 'Inconnu'}\n"
                f"**Avant** : {before.name}\n"
                f"**Après** : {after.name}"
            ))

    # === Logs pseudos ===
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Changement de pseudo
        if before.nick != after.nick:
            if not self.channels["pseudo"]:
                return
            auditor = await self.get_auditor(after.guild, discord.AuditLogAction.member_update, after)
            ch = self.get_channel("pseudo")
            if ch:
                await ch.send(embed=log_embed(
                    "📛 Pseudo changé",
                    f"**Modifié par** : {auditor.mention if auditor else after.mention}\n"
                    f"**Membre** : {after.mention}\n"
                    f"**Avant** : {before.nick or before.name}\n"
                    f"**Après** : {after.nick or after.name}"
                ))

    # === Logs bans/mutes/warns (à connecter avec tes commandes) ===
    # Ces logs seront déclenchés manuellement depuis tes cogs de modération
    # Exemple d'utilisation dans mute.py :
    # if self.bot.get_cog("ComprehensiveLogs"):
    #     log_cog = self.bot.get_cog("ComprehensiveLogs")
    #     if log_cog.channels["mute"]:
    #         ch = log_cog.get_channel("mute")
    #         await ch.send(embed=log_embed(...))

def setup(bot):
    bot.add_cog(ComprehensiveLogs(bot))