
#filename: change_focus_linux.py
#description: demonstrates how to parse a string using split, use re.matching, and does a search and replace with re.sub
import subprocess
import re
#get list of windows on the Linux desktop
#wmctrl -lG | awk -F" " {'print $5,$6,$8,$9,$10'}
#ut = getoutput('wmctrl -l -G -p -x')
def focus_window(target_string):
  output=subprocess.Popen(("wmctrl", "-p","-G","-l"),stdout=subprocess.PIPE)
  for line in output.stdout:
    parsed_line=(line.decode('utf-8').rstrip())
    print(f"debug: {parsed_line}")
    if re.search(re.escape(target_string), parsed_line):
       string_array=parsed_line.split(' ')
       id=parsed_line.split(' ')[0] #first entry is id
       out=subprocess.Popen(('wmctrl','-id','-a',id)) #change the screen using id
       return 0 #sucess
  return 1 #error



error=focus_window("VE -") #partial name
print(f"error is {error}")





