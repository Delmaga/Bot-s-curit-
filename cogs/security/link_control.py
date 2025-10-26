# cogs/security/link_control.py
from discord.ext import commands
import discord

class LinkControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_links_allowed = {}  # channel_id → bool

    @commands.command(name="lien_discord", description="Autoriser ou bloquer les liens Discord dans un salon")
    @commands.has_permissions(manage_messages=True)
    async def toggle_discord_links(self, ctx, salon: discord.TextChannel, actif: bool):
        self.discord_links_allowed[salon.id] = actif
        status = "activée" if actif else "désactivée"
        await ctx.respond(
            f"✅ Protection liens Discord **{status}** dans {salon.mention}",
            ephemeral=False
        )

    # Cette méthode peut être appelée par d'autres cogs (ex: security_logs)
    def are_discord_links_allowed(self, channel_id: int) -> bool:
        return self.discord_links_allowed.get(channel_id, True)

def setup(bot):
    bot.add_cog(LinkControl(bot))