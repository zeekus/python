
#filename: re_sub_example.py
#description: demonstrates how do a search and replace with re.sub
import re

my_string=("George Washington")
print("original string: " + my_string)
new_string=(re.sub(r'.*e','Al', my_string))
print("new string: " + new_string)



