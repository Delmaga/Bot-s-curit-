# cogs/moderation/warn.py
from discord.ext import commands
import discord
from utils.embeds import log_embed

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}  # user_id -> list of warns

    @commands.command(name="warn", description="Avertir un utilisateur")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, membre: discord.Member, *, raison: str):
        if membre.id not in self.warns:
            self.warns[membre.id] = []
        self.warns[membre.id].append({
            "reason": raison,
            "moderator": ctx.author.id
        })
        embed = log_embed(
            "⚠️ Avertissement",
            f"{membre.mention} a reçu un avertissement.\n**Raison** : {raison}"
        )
        await ctx.respond(embed=embed, ephemeral=False)

    @commands.command(name="warn_list", description="Voir les avertissements d'un utilisateur")
    @commands.has_permissions(manage_messages=True)
    async def warn_list(self, ctx, membre: discord.Member = None):
        if membre:
            user_warns = self.warns.get(membre.id, [])
            if not user_warns:
                await ctx.respond(f"📭 {membre.mention} n'a aucun avertissement.", ephemeral=False)
            else:
                desc = "\n".join(f"• {w['reason']}" for w in user_warns)
                await ctx.respond(embed=log_embed(f"📋 Avertissements de {membre}", desc), ephemeral=False)
        else:
            if not self.warns:
                await ctx.respond("📭 Aucun avertissement sur le serveur.", ephemeral=False)
            else:
                total = sum(len(w) for w in self.warns.values())
                desc = f"**Total** : {total} avertissement(s)\n"
                desc += "\n".join(
                    f"<@{uid}> : {len(warns)} warn(s)"
                    for uid, warns in list(self.warns.items())[:10]  # limite pour éviter overflow
                )
                await ctx.respond(embed=log_embed("📋 Tous les avertissements", desc), ephemeral=False)

    @commands.command(name="unwarn", description="Retirer un avertissement (pas implémenté finement)")
    @commands.has_permissions(manage_messages=True)
    async def unwarn(self, ctx, membre: discord.Member, *, raison: str = "Retrait manuel"):
        if membre.id in self.warns and self.warns[membre.id]:
            self.warns[membre.id].pop()  # retire le dernier
            if not self.warns[membre.id]:
                del self.warns[membre.id]
            await ctx.respond(embed=log_embed("✅ Unwarn", f"Un avertissement a été retiré à {membre.mention}."), ephemeral=False)
        else:
            await ctx.respond("❌ Cet utilisateur n'a pas d'avertissement à retirer.", ephemeral=False)

def setup(bot):
    bot.add_cog(WarnCog(bot))