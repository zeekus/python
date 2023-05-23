#!/usr/bin/python
# filename: beautify_apt_history.py
# description: parse file /var/apt/history.log and make it look pretty.

import re
import os
import subprocess
import magic
#note magic requires 'pip install magic-python'

debug = 0
target_filename = "/var/log/apt/history.log"


def use_magic_to_get_file_encoding(target_filename):
    try:
        with open(target_filename, "rb") as file:
            blob = file.read()
        m = magic.Magic(mime_encoding=True)
        myencoding = m.from_buffer(blob)
        print(f"Passed: encoding is '{myencoding}' on '{target_filename}'")
        return myencoding
    except FileNotFoundError:
        print(f"Failed: '{target_filename}' file not found.")
        exit(os.EX_IOERR)
    except:
        print(f"Failed when trying to determine the file encoding for our file '{target_filename}'")
        exit(os.EX_IOERR)


# Verify if the file exists or exit
if not os.path.exists(target_filename):
    print(f"Failed: '{target_filename}' file not found.")
    exit(os.EX_IOERR)
else:
    print(f"Passed: '{target_filename}' file exists.")
    hostname = os.uname().nodename
    print(f"Hostname: {hostname}")


# Main variables
e = use_magic_to_get_file_encoding(target_filename)
data_from_file = []  # array of data elements from file
upgraded_items = []  # array of upgraded_items items


try:
    with open(target_filename, "r", encoding=e) as myfile:
        for line in myfile:
            data_from_file.append(line.strip())
except FileNotFoundError:
    print(f"Error opening: {target_filename}")
    exit(os.EX_IOERR)


if debug == 1:
    print("=========================================")
    print("Data from file")
    print("=========================================")
    for line in data_from_file:
        if line:
            print(f". '{line}'")
    print("=========================================")


count = 0
st_date = ""
ed_date = ""
for line in data_from_file:
    line = line.strip()  # remove white space
    if re.search("^Start-Date:", line):
        st_date = line.split("Start-Date:")[1].strip()
    elif re.search("^Commandline:", line):
        cl = line.split(":")[1]
    elif re.search("^Requested-By:", line):
        rb = line.split(":")[1]
    elif re.search("^Upgrade:", line):  # upgraded_items items
        upgraded_items = line.split("Upgrade:")[1]
    elif re.search("^End-Date:", line):
        ed_date = line.split("End-Date:")[1].strip()
    else:
        a = 'nothing'

    my_start = st_date.split(' ')[0]  # trimmed off hours/minutes
    my_end = ed_date.split(' ')[0]  # trimmed off hours/minutes

    if my_start == my_end and len(my_start) > 1:
        print()
        count += 1
        if debug == 1:
            print(f"st and ed are {my_start}, {my_end}")
        print(f"{hostname} Update completed: {my_start}")
        print("=============================================")

        if len(upgraded_items)==0:
            print ("empty list. Exiting.")
            exit(0)
        else:
          newlist = upgraded_items.split(')')
          for line1 in newlist:
            line1 = line1.replace(',', '')  # get rid of "," at the beginning of the string
            if len(line1) > 0:
                line1 = line1.split(" (")[0].strip()  # remove the Ubuntu specific version info
                print(f"Updated '{line1}'")
