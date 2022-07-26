def format_duration(s):
    a = ''
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)

    if y > 0 : a = str(y) + ' year' + ('s' if y>1  else '')
    if d > 0 : a += (', ' if y>0 else '') + str(d) + ' day' + ('s' if d>1  else '')
    if h > 0 : a += (', ' if d>0 else '') + str(h) + ' hour' + ('s' if h>1  else '')
    if m > 0 : a += (', ' if h>0 and s>0 else '') + (' and ' if h>0 and s==0 else '') + str(m) + ' minute' + ('s' if m>1 else '')   
    if s > 0 : a += (' and ' if m>0 else '') + str(s) + ' second' + ('s' if s>1  else '') 
    return 'now' if not(a) else a 
