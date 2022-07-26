per = (31536000, 86400, 3600, 60, 1)
per2 = (' year', ' day', ' hour', ' minute', ' second')


def format_duration(seconds):
    if not seconds:
        return 'now'
    res = []
    for i in range(5):
        q = seconds // per[i]
        if q:
            res.append(str(q) + per2[i] + ('s' if q > 1 else ''))
            seconds -= per[i] * q
    if len(res) > 1:
        res[-1] = res[-2] + ' and ' + res.pop()
    return ', '.join(res)
