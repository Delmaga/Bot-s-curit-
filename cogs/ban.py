from discord.ext import commands
import discord
import asyncio
from utils.embeds import log_embed
from utils.time_parser import parse_time

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_bans = {}

    @commands.slash_command(name="ban", description="Bannir un utilisateur temporairement")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membre: discord.Member, temps: str, raison: str):
        if membre.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ Tu ne peux pas bannir cet utilisateur.", ephemeral=False)
            return

        seconds = parse_time(temps)
        await membre.ban(reason=raison)
        self.temp_bans[membre.id] = {"end_time": asyncio.get_event_loop().time() + seconds, "reason": raison}

        embed = log_embed(
            "🔨 Ban temporaire",
            f"**Utilisateur** : {membre.mention}\n"
            f"**Durée** : {temps}\n"
            f"**Raison** : {raison}\n"
            f"**Modérateur** : {ctx.author.mention}"
        )
        await ctx.respond(embed=embed, ephemeral=False)

        await asyncio.sleep(seconds)
        try:
            await ctx.guild.unban(membre)
            self.temp_bans.pop(membre.id, None)
        except:
            pass

    @commands.slash_command(name="unban", description="Débannir un utilisateur par ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await ctx.guild.unban(user)
            await ctx.respond(embed=log_embed("✅ Unban", f"{user} a été débanni."), ephemeral=False)
        except ValueError:
            await ctx.respond("❌ ID invalide.", ephemeral=False)
        except discord.NotFound:
            await ctx.respond("❌ Cet utilisateur n'est pas banni.", ephemeral=False)

    @commands.slash_command(name="ban_list", description="Liste des bans temporaires actifs")
    @commands.has_permissions(ban_members=True)
    async def ban_list(self, ctx):
        if not self.temp_bans:
            await ctx.respond("📭 Aucun ban temporaire actif.", ephemeral=False)
            return
        desc = "\n".join(f"<@{user_id}> : {data['reason']}" for user_id, data in self.temp_bans.items())
        await ctx.respond(embed=log_embed("📋 Bans actifs", desc[:4000]), ephemeral=False)

def setup(bot):
    bot.add_cog(BanCog(bot))