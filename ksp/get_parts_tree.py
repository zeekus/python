
#!/usr/bin/python
#filename: get_parts_tree_in_vessel.py
#Description: changes active vessel and gets list of vessels availabe in KSP


import krpc
import re #regular expression match
conn = krpc.connect()
vessel = conn.space_center.active_vessel
debug=0 #change to 1 to see what the object are doing

root = vessel.parts.root
stack = [(root, 0)]
layer=1
newstack=[]
if debug==1: print("stack is an object {}".format(stack))
if debug==1: print("root is {}".format(root))
while stack:
    part, stage = stack.pop()
    if debug==1: print("debug1: parent_object: {} stage: {}".format(part,stage))
    newstack.append("{} {}".format(layer*stage, part.title)) #build new array with parts as strings

    #print(layer*stage, part.title)
    for child in part.children:
      stack.append((child, stage+1))
      if debug==1: print("debug2: child_object: {}, stage: {}".format(child,stage+1))

#sort parts in order from Root 0
newstack=sorted(newstack)

for line in newstack:
    p=re.compile(r"^0") #find root object start with 0
    if p.match(line):
      print ("'{}'".format(line.split("0 ")[1])) #remove space
    else:
      print(line)
