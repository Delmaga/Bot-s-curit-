# cogs/protection.py
from discord.ext import commands
import discord
import re
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta
from utils.embeds import log_embed

class ProtectionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.insulte_active = False
        self.spam_active = False
        self.insulte_log_channel_id = None
        self.spam_log_channel_id = None

        # Liste d'insultes (à compléter)
        self.insultes = {
            "fdp", "fils de pute", "ntm", "nique ta mère", "tg", "ta gueule",
            "connard", "connasse", "salaud", "salope", "merde", "pute", "bitch"
        }

        # Anti-spam
        self.spam_tracker = defaultdict(deque)  # user_id -> [timestamps]
        self.warn_count = defaultdict(int)      # user_id -> count
        self.muted_users = set()                # user_id déjà mute

    def normalize_text(self, text):
        """Nettoie le texte : minuscules, supprime . - _ etc."""
        return re.sub(r'[^a-z0-9]', '', text.lower())

    def contains_insult(self, text):
        normalized = self.normalize_text(text)
        for insult in self.insultes:
            clean_insult = self.normalize_text(insult)
            if clean_insult in normalized:
                return insult
        return None

    @commands.slash_command(name="logs_inulte", description="Définir le salon pour les logs d'insultes")
    @commands.has_permissions(administrator=True)
    async def set_insulte_log(self, ctx, salon: discord.TextChannel):
        self.insulte_log_channel_id = salon.id
        await ctx.respond(f"✅ Salon logs insultes : {salon.mention}", ephemeral=False)

    @commands.slash_command(name="logs_spam", description="Définir le salon pour les logs de spam")
    @commands.has_permissions(administrator=True)
    async def set_spam_log(self, ctx, salon: discord.TextChannel):
        self.spam_log_channel_id = salon.id
        await ctx.respond(f"✅ Salon logs spam : {salon.mention}", ephemeral=False)

    @commands.slash_command(name="insulte", description="Activer/désactiver l'anti-insulte")
    @commands.has_permissions(manage_messages=True)
    async def toggle_insulte(self, ctx, actif: bool):
        self.insulte_active = actif
        await ctx.respond(f"✅ Anti-insulte {'activé' if actif else 'désactivé'}", ephemeral=False)

    @commands.slash_command(name="anti_spam", description="Activer/désactiver l'anti-spam")
    @commands.has_permissions(manage_messages=True)
    async def toggle_spam(self, ctx, actif: bool):
        self.spam_active = actif
        await ctx.respond(f"✅ Anti-spam {'activé' if actif else 'désactivé'}", ephemeral=False)

    async def mute_user(self, member, reason="Spam"):
        role = discord.utils.get(member.guild.roles, name="Muted")
        if not role:
            role = await member.guild.create_role(name="Muted", reason="Rôle anti-spam")
            for channel in member.guild.channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False)
        await member.add_roles(role, reason=reason)

        # Log spam
        if self.spam_log_channel_id:
            ch = self.bot.get_channel(self.spam_log_channel_id)
            if ch:
                await ch.send(embed=log_embed(
                    "🔇 Mute pour spam",
                    f"**Utilisateur** : {member.mention}\n"
                    f"**Raison** : {reason}\n"
                    f"**Durée** : 3 heures"
                ))

        # Auto-unmute après 3h
        await asyncio.sleep(3 * 3600)
        if role in member.roles:
            await member.remove_roles(role)
            self.muted_users.discard(member.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        # === ANTI-INSULTE ===
        if self.insulte_active and self.insulte_log_channel_id:
            insult = self.contains_insult(message.content)
            if insult:
                await message.delete()
                await message.author.send("❌ Les insultes ne sont pas autorisées sur ce serveur.")
                
                ch = self.bot.get_channel(self.insulte_log_channel_id)
                if ch:
                    await ch.send(embed=log_embed(
                        "⚠️ Insulte détectée",
                        f"**Auteur** : {message.author.mention} (`{message.author.id}`)\n"
                        f"**Contenu** : `{message.content}`\n"
                        f"**Insulte trouvée** : `{insult}`\n"
                        f"**Salon** : {message.channel.mention}"
                    ))

        # === ANTI-SPAM ===
        if self.spam_active:
            user_id = message.author.id
            now = datetime.utcnow()

            # Nettoyer les timestamps plus vieux que 2 secondes
            while self.spam_tracker[user_id] and now - self.spam_tracker[user_id][0] > timedelta(seconds=2):
                self.spam_tracker[user_id].popleft()

            self.spam_tracker[user_id].append(now)

            if len(self.spam_tracker[user_id]) >= 5 and user_id not in self.muted_users:
                self.warn_count[user_id] += 1
                remaining = 3 - self.warn_count[user_id]

                if remaining > 0:
                    await message.author.send(
                        f"⚠️ Merci de ne pas spammer. Il vous reste **{remaining} avertissement(s)** avant un mute de 3h."
                    )
                    
                    if self.spam_log_channel_id:
                        ch = self.bot.get_channel(self.spam_log_channel_id)
                        if ch:
                            await ch.send(embed=log_embed(
                                "📨 Avertissement spam",
                                f"**Utilisateur** : {message.author.mention}\n"
                                f"**Nombre de messages** : {len(self.spam_tracker[user_id])}\n"
                                f"**Avertissements** : {self.warn_count[user_id]}/3"
                            ))
                else:
                    await self.mute_user(message.author, reason="Spam (3 avertissements)")
                    self.warn_count[user_id] = 0  # reset après mute
                    self.muted_users.add(user_id)

def setup(bot):
    bot.add_cog(ProtectionCog(bot))