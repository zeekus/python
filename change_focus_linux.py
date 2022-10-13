import subprocess
import re
#get list of windows on the Linux desktop
output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    if re.search("EVE -", parsed_line):
         print (parsed_line.split(' '))
         
