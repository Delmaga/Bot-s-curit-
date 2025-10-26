# cogs/moderation/mute.py
from discord.ext import commands
import discord
import asyncio
import time
from utils.embeds import log_embed
from utils.time_parser import parse_time

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muted_users = {}

    async def get_mute_role(self, guild):
        role = discord.utils.get(guild.roles, name="Muted")
        if not role:
            role = await guild.create_role(name="Muted", reason="Rôle pour mute")
            for channel in guild.channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False)
        return role

    @commands.command(name="mute")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, membre: discord.Member, temps: str, *, raison: str):
        if membre.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ Tu ne peux pas mute cet utilisateur.")
            return

        role = await self.get_mute_role(ctx.guild)
        await membre.add_roles(role, reason=raison)
        seconds = parse_time(temps)
        self.muted_users[membre.id] = {"end_time": time.time() + seconds, "reason": raison}

        embed = log_embed(
            "🔇 Mute appliqué",
            f"**Utilisateur** : {membre.mention}\n"
            f"**Durée** : {temps}\n"
            f"**Raison** : {raison}\n"
            f"**Modérateur** : {ctx.author.mention}"
        )
        await ctx.send(embed=embed)

        await asyncio.sleep(seconds)
        if role in membre.roles:
            await membre.remove_roles(role)
            self.muted_users.pop(membre.id, None)

    @commands.command(name="unmute")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, membre: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role and role in membre.roles:
            await membre.remove_roles(role)
            self.muted_users.pop(membre.id, None)
            await ctx.send(embed=log_embed("🔊 Unmute", f"{membre.mention} n'est plus mute."))
        else:
            await ctx.send("❌ Cet utilisateur n'est pas mute.")

    @commands.command(name="mute_list")
    @commands.has_permissions(manage_messages=True)
    async def mute_list(self, ctx):
        if not self.muted_users:
            await ctx.send("📭 Aucun mute actif.")
            return
        desc = "\n".join(f"<@{uid}> : {data['reason']}" for uid, data in self.muted_users.items())
        await ctx.send(embed=log_embed("📋 Mutes actifs", desc[:4000]))

async def setup(bot):
    await bot.add_cog(MuteCog(bot))