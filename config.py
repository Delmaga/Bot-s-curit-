# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GIVEAWAY_BOT_ID = int(os.getenv("GIVEAWAY_BOT_ID", 0))  # 0 si non défini