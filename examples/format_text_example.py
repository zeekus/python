#filename: format_text_example.py
#description: how to format text so all gaps equal each other.

import random

for x in range(100):
    percent=random.randint(1,100)*.01
    if float(percent) < 0.10:
      message=("{:-9} counT... {:4.2%}".format(x,percent)) #add an extra space so every lines up
      print(message + " -- lower than 10%")
    elif float(percent) > 0.99:
      print("{:-9} count. {:4.2%}".format(x,percent)) #remove an extra space
    else:
      print("{:-9} count.. {:4.2%}".format(x,percent))
