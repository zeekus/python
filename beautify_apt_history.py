#!/usr/bin/python
# filename: beautify_apt_history.py
# description: parse file /var/apt/history.log and make it look pretty.

import re
import os
import subprocess
import chardet
import datetime
import shutil


debug = 0
target_filename = "/var/log/apt/history.log"

# Function to get today's date
def get_todays_date():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

# Function to copy Debian package locally
def copy_debian_package(package_name):
    today = get_todays_date()
    destination_directory = f"/var/tmp/{today}_update"
    os.makedirs(destination_directory, exist_ok=True)

    os.chdir(destination_directory) #change to the destination directory
   
    #subprocess.run(['apt-get', 'download', package_name, '-o', f'dir::cache={destination_directory}'])

    subprocess.run(['apt-get', 'download', package_name ]) # Run the apt-get download command

#use chardet to get file encoding info
def use_chardet_to_get_file_encoding(target_filename):
    try:
        with open(target_filename, "rb") as file:
            blob = file.read()
        result = chardet.detect(blob)
        myencoding = result["encoding"]
        print(f"Passed: encoding is '{myencoding}' on '{target_filename}'")
        return myencoding
    except FileNotFoundError:
        print(f"Failed: '{target_filename}' file not found.")
        exit(os.EX_IOERR)
    except:
        print(f"Failed when trying to determine the file encoding for our file '{target_filename}'")
        exit(os.EX_IOERR)


#use magic libary to get file encoding info
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
e = use_chardet_to_get_file_encoding(target_filename)
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

if len(upgraded_items)>0:
   print(f"{hostname} Update completed: {my_start}")
   #print(upgraded_items)
   newlist = upgraded_items.split(')')
   for line1 in newlist:
       line1 = line1.replace(',', '')  # get rid of "," at the beginning of the string
       if len(line1) > 0:
         line1 = line1.split(" (")[0].strip()  # remove the Ubuntu specific version info
         print(f"Updated '{line1}'")
         if re.match(r'kugutsu', hostname): # Add the regular expression pattern to match the hostname
           copy_debian_package(line1)  # Call the function to copy the Debian package
