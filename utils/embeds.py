# utils/embeds.py
from discord import Embed
from datetime import datetime

def log_embed(title: str, description: str) -> Embed:
    """Embed minimaliste, transparent (noir = fond transparent), sans bleu."""
    embed = Embed(
        title=title,
        description=description,
        color=0x000000,  # Transparent dans Discord
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text="Seïko • Sécurité")
    return embed