#!/usr/bin/python3
#filename: password_gen.py
#description: random password generator first attempt for lambda
length=(50-2)#20 characters

import random
# Character range function
def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))

def stringToList(string):
    lisRes=[]
    for char in string:
        lisRes.append(char)
    return lisRes

def lambda_handler( event, context ):
  # Example run
  mylist=[]
  special_list=stringToList('.!@#$^&*()')#simplied special characters
  #print(str(special_list))

  for character in range_char("a", "z"):
    mylist.append(character)
    mylist.append(character.upper())

  num=random.randrange(0,9,1)
  char=(special_list[num])
  random.shuffle(mylist)

  count=0
  num_added=0
  special_added=0
  pass_string=""
  while count<length:
    pass_string=(str(pass_string) + str(mylist[count]) )
    count=count+1

  return pass_string=(str(num) + str(pass_string) + str(char))

pass_string=lambda_handler()
print("password is:" + pass_string)





