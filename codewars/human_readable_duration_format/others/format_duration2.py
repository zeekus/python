def format_duration(seconds):
    if seconds == 0: return 'now'
    y, seconds = divmod(seconds, 60 * 60 * 24 * 365 )
    d, seconds = divmod(seconds, 60 * 60 * 24 )
    h, seconds = divmod(seconds, 60 * 60 )
    m, seconds = divmod(seconds, 60 )
    s = seconds
    time_list = [str(x) + ' ' + y + ('s' if x > 1 else '') for x, y in zip([y,d,h,m,s], ['year','day','hour','minute','second']) if x > 0]
    return ', '.join(time_list[:-2] + [' and '.join(time_list[-2:])])
