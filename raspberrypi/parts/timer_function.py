import time

def start_timer():
    return time.time()

def stop_timer(start_time):
    return time.time() - start_time

start_time = start_timer()

# Code block to be timed
time.sleep(3900)

elapsed_time = stop_timer(start_time)
hours, remainder = divmod(elapsed_time, 3600)
minutes, seconds = divmod(remainder, 60)
print(f"Raw: Elapsed time: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

if elapsed_time < 60:     #1 minute
  print(f"Elapsed seconds: {int(seconds)}")
elif elapsed_time < 3600: #1 hour
  print(f"Elapsed minutes:{int(minutes)} seconds:{int(seconds)}")
else:
  print(f"Elapsed hours:{int(hours)} minutes:{int(minutes)} seconds:{int(seconds)}")


