import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

filename = "door_data.txt"
data = []

with open(filename, "r") as file:
    for line in file.readlines():
        data.append(line.strip())

timestamps = []
durations = []
cumulative_time = []

current_hour = None
cumulative = 0

for line in data:
    parts = line.split(" - ")
    timestamp_str, duration_str = parts[0], parts[1].split()[7]
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    duration = float(duration_str) / 60
    
    if current_hour is None or timestamp.hour != current_hour:
        current_hour = timestamp.hour
        cumulative = 0
    
    cumulative += duration
    timestamps.append(timestamp)
    durations.append(duration)
    cumulative_time.append(cumulative)

fig, ax = plt.subplots()
ax.plot(timestamps, cumulative_time)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

plt.xlabel("Timestamp (HH:MM)")
plt.ylabel("Cumulative Time (minutes)")
plt.title("Cumulative Minutes the Door is Open per Hour")
plt.xticks(rotation=45)
plt.show()
