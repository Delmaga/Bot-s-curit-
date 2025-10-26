# utils/time_parser.py
import re

def parse_time(time_str: str) -> int:
    """Convertit '5m', '2h30m', '1d' en secondes."""
    time_str = time_str.lower().strip()
    total_seconds = 0
    matches = re.findall(r'(\d+)\s*([mhd])', time_str)
    for amount, unit in matches:
        amount = int(amount)
        if unit == 'm':
            total_seconds += amount * 60
        elif unit == 'h':
            total_seconds += amount * 3600
        elif unit == 'd':
            total_seconds += amount * 86400
    return total_seconds if total_seconds > 0 else 300  # 5 min par défaut