# cogs/moderation/mute.py
from discord.ext import commands
import discord
from utils.embeds import log_embed
from utils.time_parser import parse_time
import asyncio

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muted_users = {}  # En production → utiliser une base de données

    async def get_mute_role(self, guild):
        role = discord.utils.get(guild.roles, name="Muted")
        if not role:
            role = await guild.create_role(name="Muted", reason="Rôle pour mute")
            for channel in guild.channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False)
        return role

    @commands.slash_command(name="mute", description="Mute un utilisateur temporairement")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, membre: discord.Member, temps: str, *, raison: str):
        if membre.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ Tu ne peux pas mute cet utilisateur.", ephemeral=False)
            return

        role = await self.get_mute_role(ctx.guild)
        await membre.add_roles(role, reason=raison)
        seconds = parse_time(temps)
        self.muted_users[membre.id] = {
            "end_time": ctx.bot.loop.time() + seconds,
            "reason": raison,
            "moderator": ctx.author.id
        }

        embed = log_embed(
            "🔇 Mute appliqué",
            f"**Utilisateur** : {membre.mention}\n"
            f"**Durée** : {temps}\n"
            f"**Raison** : {raison}\n"
            f"**Modérateur** : {ctx.author.mention}"
        )
        await ctx.respond(embed=embed, ephemeral=False)

        # Auto-unmute
        await asyncio.sleep(seconds)
        if role in membre.roles:
            await membre.remove_roles(role)
            self.muted_users.pop(membre.id, None)

    @commands.slash_command(name="unmute", description="Retirer le mute d'un utilisateur")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, membre: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role and role in membre.roles:
            await membre.remove_roles(role)
            self.muted_users.pop(membre.id, None)
            await ctx.respond(embed=log_embed("🔊 Unmute", f"{membre.mention} n'est plus mute."), ephemeral=False)
        else:
            await ctx.respond("❌ Cet utilisateur n'est pas mute.", ephemeral=False)

    @commands.slash_command(name="mute_list", description="Liste des utilisateurs actuellement mute")
    @commands.has_permissions(manage_messages=True)
    async def mute_list(self, ctx):
        if not self.muted_users:
            await ctx.respond("📭 Aucun utilisateur n'est mute.", ephemeral=False)
            return
        desc = "\n".join(
            f"<@{user_id}> : {data['reason']}"
            for user_id, data in self.muted_users.items()
        )
        await ctx.respond(embed=log_embed("📋 Mutes actifs", desc[:4000]), ephemeral=False)

def setup(bot):
    bot.add_cog(MuteCog(bot))