import re

myline="[ 2022.11.21 02:27:58 ] (None) Jumping from Niyabainen to Tunttaras"
target="jumping"
gametime="2022.11.21 02:27:58"

log_line_parsed=myline.replace(' (','|')#convert " (" to | 
log_line_parsed=log_line_parsed.replace(') ','|')#convert  ") " to |
gt,mtype,message=log_line_parsed.split("|")
gt=gt.replace('[ ','').replace(' ]','') #remove both [ ] around text
print (f"cleaned up line: {gt} {mtype} {message}")
if re.search(r''.format(gametime),myline) and re.search(r''.format(target),myline):
    print (gametime)

