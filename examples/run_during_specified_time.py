#filename: run_during_specified_time.py
#description: run a function during a specified time using OS and datetime library.


import datetime
import os

# Get the current local time
current_time = datetime.datetime.now().time()

# Define the start and end times in EST
start_time = datetime.time(7, 0)  # 7 AM EST
end_time = datetime.time(11, 0)  # 8 AM EST

# Check if the current time is in the specified time zone
env_tz = os.environ.get('TZ')  # Get the value of the TZ environment variable

if env_tz and 'EST' in env_tz:
    # Time zone is specified as EST
    est_offset = datetime.timedelta(hours=5)
else:
    # Time zone is not specified or different from EST
    est_offset = datetime.timedelta(hours=0)

# Calculate the adjusted time in the specified time zone
current_datetime = datetime.datetime.now()
current_datetime_est = current_datetime - est_offset

# Check if the current time is between the start and end times in the specified time zone
print(f"debug: current_time is {current_time}")
print(f"debug: current_datetime_est is {current_datetime_est.time()}")

if start_time <= current_datetime_est.time() <= end_time:
    print("Hello World")
else:
    print("Not during run time")

