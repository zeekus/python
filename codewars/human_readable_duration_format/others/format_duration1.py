import re
def format_duration(seconds):
    if not seconds: return 'now'
    minutes = seconds / 60
    seconds %= 60
    hours = minutes / 60
    minutes %= 60
    days = hours / 24
    hours %= 24
    years = days / 365
    days %= 365
    a = []
    for n, l in zip([years, days, hours, minutes, seconds], ['year', 'day', 'hour', 'minute', 'second']):
        if n == 1:
            a.append('%d %s' % (n, l))
        elif n > 1:
            a.append('%d %ss' % (n, l))
    return re.sub(r', ([^,]*)$', lambda o: ' and ' + o.group(1), ', '.join(a))
