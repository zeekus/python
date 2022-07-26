def format_duration(seconds: int) -> str:
    if not seconds:
        return 'now'

    time = {
        'year':   seconds // (60 * 60 * 24 * 365),
        'day':    seconds // (60 * 60 * 24) % 365,
        'hour':   seconds // (60 * 60) % 24,
        'minute': seconds // 60 % 60,
        'second': seconds % 60,
    }

    *chunks, last = [f'{val} {item}' + 's'*(val != 1) for item, val in time.items() if val]
    return ', '.join(chunks) + ' and ' + last if chunks else last
