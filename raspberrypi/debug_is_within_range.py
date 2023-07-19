import datetime
import os

def is_within_time_range(start_hour, start_min, end_hour, end_min):
    # Get the current local time and date
    current_datetime = datetime.datetime.now()

    # Check if the current time is in the specified time zone
    env_tz = os.environ.get('TZ')  # Get the value of the TZ environment variable

    if env_tz and 'EST' in env_tz:
        # Time zone is specified as EST
        est_offset = datetime.timedelta(hours=5)
    else:
        # Time zone is not specified or different from EST
        est_offset = datetime.timedelta(hours=0)

    # Calculate the adjusted time in the specified time zone
    current_datetime_est = current_datetime - est_offset

    # Check if the current time is between the start and end times in the specified time zone
    print(f"debug: current_time is {current_datetime_est.strftime('%H:%M')}")

    # Create datetime objects for start and end times
    start_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(start_hour, start_min, 0))
    end_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(end_hour, end_min, 0))

    # Check if the end time is before the start time
    if end_datetime < start_datetime:
        # Increment the end day by one
        end_datetime += datetime.timedelta(days=1)

    if start_datetime <= current_datetime <= end_datetime:
        return True
    return False

start_hour = 22
start_min = 30
end_hour = 13
end_min = 0

print(f"baseline: {start_hour:02d}:{start_min:02d} to {end_hour:02d}:{end_min:02d}")
result = is_within_time_range(start_hour, start_min, end_hour, end_min)
print(f"result is {result}")