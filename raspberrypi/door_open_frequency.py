import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

filename = "door_data.txt"
data = []

with open(filename, "r") as file:
    for line in file.readlines():
        data.append(line.strip())

door_openings = {}  # Dictionary to store the number of door openings per hour
total_openings = 0  # Total number of door openings

for line in data:
    parts = line.split(" - ")
    timestamp_str, duration_str = parts[0], parts[1].split()[7]
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    hour = timestamp.strftime("%H")
    if hour not in door_openings:
        door_openings[hour] = 0
    door_openings[hour] += 1
    total_openings += 1

hours = sorted(door_openings.keys())
frequencies = [door_openings[hour] for hour in hours]

fig, ax = plt.subplots()
ax.plot(hours, frequencies, marker='o')
ax.set_xticks(hours)
ax.set_xlabel("Hour")
ax.set_ylabel("Number of Door Openings")
ax.set_title("Hourly Trend of Door Openings\nTotal Openings: {}".format(total_openings))

plt.show()
