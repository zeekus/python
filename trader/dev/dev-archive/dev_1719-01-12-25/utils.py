# utils.py
from datetime import datetime

def format_trade_runtime(start_dt, end_dt):
    """Return a string representing how long the trade was open in days/hours/min/secs."""
    if not start_dt or not end_dt:
        return "N/A"
    diff = end_dt - start_dt
    total_sec = diff.total_seconds()
    days = int(total_sec // 86400)
    remainder = int(total_sec % 86400)
    hours = remainder // 3600
    remainder %= 3600
    minutes = remainder // 60
    seconds = remainder % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

