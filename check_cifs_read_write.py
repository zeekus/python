#!/bin/python
#filename: check_cifs_read_write.py
#description: checks the cifs and sends an email if there is an issue.

import sys
import os
import re
import subprocess
import datetime

# Generate a timestamp in the format YYYYMMDD_HHMMSS
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Update the file name with the timestamp
file_name = "cifstests_{}.txt".format(timestamp)
script_name = os.path.basename(__file__) #name of this file. 

# Global variables
error_count = 0
email_recipient = 'myuser@example.net'
email_subject = "CIFS Write Failure"
data = [""] #data for body of the email 
SERVERNAME=os.uname().nodename if hasattr(os, 'uname') else os.getenv('HOSTNAME', os.getenv('COMPUTERNAME')) #get hostname of server 
imagery_file_path = "/media/imagery/{}".format(file_name)
media_file_path = "/media/share/GIS/{}".format(file_name)

#def read_lines_from_file(file_path):
#    """Read lines from a file and return them as a list."""
#    with open(file_path) as file:
#        lines = file.readlines()
#    return lines

def write_lines_to_file(file_path, lines):
    """Write lines to a file."""
    with open(file_path, mode="w") as file:
        for line in lines:
            file.write(line.rstrip() + "\n")

def write_file_with_error_handling(file_path, lines):
    """Write lines to a file with error handling."""
    try:
        print("Writing to file: {}".format(file_path))
        write_lines_to_file(file_path, lines)
    except IOError as e:
        print("Error writing to file: {}".format(file_path))
        global error_count
        error_count += 1

def remove_file_with_error_handling(file_path):
    """Remove a file with error handling."""
    try:
        os.remove(file_path)
        print("File removed: {}".format(file_path))
    except OSError as e:
        print("Error removing file: {}".format(file_path))
        global error_count
        error_count += 1
		
print ("debug info on {}.".format(script_name))
print(imagery_file_path)
print(media_file_path)

write_file_with_error_handling(imagery_file_path, data)
write_file_with_error_handling(media_file_path, data)

if error_count > 0:
    df_output = subprocess.check_output(["df", "-h"]).decode('utf-8')
    message = "Errors occurred during CIFS file writes on {}. This may indicate an unmounted filesystem.\nError count: {}\n{}".format(SERVERNAME, error_count, df_output)
    print(message)
    os.system("echo '{}' | mutt -s '{}' {}".format(message, email_subject, email_recipient))
else:
    print("Success. No errors occurred during the writes on {}.".format(SERVERNAME))


remove_file_with_error_handling(imagery_file_path)
remove_file_with_error_handling(media_file_path)