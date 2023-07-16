import datetime
import time
#filename: 5_second_stop_watch.py
#description: use the datetime module to create a 5 second stop watch.

# Time Tracking
start_time = datetime.datetime.now().time()
reset_interval = datetime.timedelta(seconds=5)  # 5 seconds

# Keep the program running
while True:
    time.sleep(0.1)
    current_time = datetime.datetime.now().time()

    # Calculate elapsed time as a timedelta object
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), start_time)

    print(f"debug elapsed time: {elapsed_time}")

    # Reset bounce counts every 5 seconds
    if elapsed_time >= reset_interval:
        formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"reset {formatted_time}")
        start_time = current_time

