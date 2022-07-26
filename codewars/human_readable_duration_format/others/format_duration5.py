def format_duration(seconds):
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    year = 365 * day
    times = [year, day, hour, minute, 1]
    units = ["year", "day", "hour", "minute", "second"]
    components = []
    for time, unit in zip(times, units):
        duration, seconds = divmod(seconds, time)
        if duration > 1:
            components.append(str(duration) + " " + unit + "s")
        elif duration == 1:
            components.append(str(duration) + " " + unit)
    if len(components) == 0:
        return "now"
    elif len(components) == 1:
        return components[-1]
    else:
        return ", ".join(components[:-1]) + " and " + components[-1]
