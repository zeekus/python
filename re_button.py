import re
string="align button"
match = re.search('align', string)
print(str(match))
if match:
    print(string)

