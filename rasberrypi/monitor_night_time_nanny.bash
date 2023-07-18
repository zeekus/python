#!/bin/bash
#filename: monitor_night_time_nanny_script.bash
#description: start monitor script if it dies.


monitor_log="$(date +"%Y-%m-%d-monitor.log")"
mydate=$(date)
if ! pgrep -f "python night_time_nanny.py" > /dev/null; then
    echo "night_time_nanny.py is not running. Starting it..."
    if [ -f /home/ted/night_time_nanny.lock ]; then
      echo "$mydate found lock file removing" >> $monitor_log
      rm /home/ted/night_time_nanny.lock
    fi
    mydate=$(date)
    echo "$mydate starting nanny_cron_wrapper.py" >> $monitor_log
    #starting wrapper program
    python3 nanny_cron_wrapper.py & 
else
    echo "$mydate nanny_cron_wrapper.py is running" >> $monitor_log
fi
