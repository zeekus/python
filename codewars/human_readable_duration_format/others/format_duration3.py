def format_duration(seconds):
    td = {
        "year": seconds // 31536000,
        "day": seconds % 31536000 // 86400,
        "hour": seconds % 86400 // 3600,
        "minute": seconds % 3600 // 60,
        "second": seconds % 60,
    }

    r = [str(v) + " " + add_s(v, k) for k, v in td.items() if v > 0]

    return ' and '.join(', '.join(r).rsplit(', ', 1)) or 'now'
    
def add_s(c, s):
    if c > 1:
        return s + 's'
    return s

