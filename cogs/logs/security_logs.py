# cogs/logs/security_logs.py
from discord.ext import commands
import discord
import re
from utils.embeds import log_embed

class SecurityLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = None
        self.alert_role_id = None
        self.discord_links_allowed = {}  # salon_id → bool

    @commands.slash_command(name="logs_securite", description="Définir salon + rôle pour les alertes sécurité")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, salon: discord.TextChannel, role: discord.Role):
        self.log_channel_id = salon.id
        self.alert_role_id = role.id
        await ctx.respond(f"✅ Logs sécurité → {salon.mention} + ping {role.mention}", ephemeral=False)

    @commands.slash_command(name="lien_discord", description="Autoriser/interdire les liens Discord dans un salon")
    @commands.has_permissions(manage_messages=True)
    async def toggle_discord_links(self, ctx, salon: discord.TextChannel, actif: bool):
        self.discord_links_allowed[salon.id] = actif
        await ctx.respond(
            f"✅ Liens Discord {'autorisés' if actif else 'bloqués'} dans {salon.mention}",
            ephemeral=False
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.log_channel_id:
            return

        content = message.content.lower()
        ch = self.bot.get_channel(self.log_channel_id)
        if not ch:
            return

        # Détection de liens
        if "http" in content:
            # Vérifie si liens Discord sont autorisés dans ce salon
            if not self.discord_links_allowed.get(message.channel.id, True):
                # Log même si bloqué
                role_ping = f"<@&{self.alert_role_id}>" if self.alert_role_id else "@moderators"
                await ch.send(embed=log_embed(
                    "🔗 Lien bloqué (mais détecté)",
                    f"{role_ping} — {message.author.mention} a tenté d’envoyer un lien dans {message.channel.mention} :\n"
                    f"```{message.content}```"
                ))

        # Comptes suspects : création récente + comportement bizarre
        account_age = (discord.utils.utcnow() - message.author.created_at).days
        if account_age < 3 and len(message.content) > 50 and any(c in message.content for c in "!@#$%^&*()_+={}[]|\\:;\"'<>?,./"):
            role_ping = f"<@&{self.alert_role_id}>" if self.alert_role_id else "@moderators"
            await ch.send(embed=log_embed(
                "⚠️ Compte suspect détecté",
                f"{role_ping} — {message.author.mention} (`{message.author.id}`) a un compte de **{account_age} jour(s)** et a envoyé un message inhabituel :\n"
                f"```{message.content[:500]}```"
            ))

def setup(bot):
    bot.add_cog(SecurityLogs(bot))