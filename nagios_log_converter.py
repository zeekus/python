#!/usr/bin/env python3
#filename: nagios_log_converter.py
#use: cat /var/log/nagios4/nagios.log | python3 nagios_log_converter.py 
#descrption: this program parses out the Unix epoch time and makes it humanly readable. 

import sys
import re
from datetime import datetime
import pytz

def convert_to_est(input_stream, output_stream):
    # Define the timezone for EST
    est_tz = pytz.timezone('US/Eastern')

    # Regular expression to match Nagios log timestamp
    timestamp_pattern = r'\[(\d{10})\]'

    for line in input_stream:
        # Find the timestamp in the line
        match = re.search(timestamp_pattern, line)
        if match:
            unix_timestamp = int(match.group(1))
            # Convert Unix timestamp to datetime object
            utc_time = datetime.utcfromtimestamp(unix_timestamp)
            # Make the datetime object timezone-aware (UTC)
            utc_time = pytz.utc.localize(utc_time)
            # Convert to EST
            est_time = utc_time.astimezone(est_tz)
            # Format the new timestamp
            new_timestamp = est_time.strftime('[%Y-%m-%d %H:%M:%S %Z]')
            # Replace the old timestamp with the new one
            new_line = re.sub(timestamp_pattern, new_timestamp, line)
            output_stream.write(new_line)
        else:
            # If no timestamp found, write the original line
            output_stream.write(line)

if __name__ == "__main__":
    convert_to_est(sys.stdin, sys.stdout)