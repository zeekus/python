from datetime import datetime
import time

mytime = "11.19.2022 01:01:09"
d = datetime.strptime(mytime, "%m.%d.%Y %H:%M:%S")
s=time.mktime(d.timetuple())

print(f"Seconds from epoch: {s}") 


