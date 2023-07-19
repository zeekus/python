#!/bin/bash
#filename: monitor_night_time_nanny_script.bash
#description: start monitor script if it dies.


monitor_log="$(date +"%Y-%m-%d-monitor.log")"
mydate=$(date)
program="night_time_nanny.py"
if ! pgrep -f "python night_time_nanny.py" > /dev/null; then
    echo "$program is not running. Starting it..."
    mydate=$(date)
    echo "$mydate starting $program" >> $monitor_log
    python $program >> $monitor_log 2>&1
else
    echo "$mydate $program is running" >> $monitor_log
fi
