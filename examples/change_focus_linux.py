
#filename: change_focus_linux.py
#description: demonstrates how to parse a string using split, use re.matching, and does a search and replace with re.sub
import subprocess
import re
#get list of windows on the Linux desktop
#wmctrl -lG | awk -F" " {'print $5,$6,$8,$9,$10'}
output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    if re.search("EVE -", parsed_line):
         string_array=parsed_line.split(' ')
         w=parsed_line.split(' ')[14] #screen width
         h=parsed_line.split(' ')[15] #screen height
         screen_size=[w,h]
         window_title=re.sub(r'.*EV','EV',parsed_line)
         print (window_title)
         out=subprocess.Popen(('wmctrl','-a',window_title)) #change the screen focus

