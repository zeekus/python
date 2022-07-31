import re
def check_friendly(name_fields):
  #example friendly ships use 3 letter call sign followed by 3 numbers that add up to 15
  #name_fields=['ZRI', '618', 'Slacker']
  pattern=re.compile("[a-zA-Z]+")#letter pattern
  print("check for a three letter call sign with a-z patern match")
  if len(name_fields[0]) == 3 and len(name_fields[1]) ==3 and pattern.fullmatch(name_fields[0]) is not None:
       #3 letter call sign found
       #find sum of 3 number signifier
       my_sum=(sum(int(a) for a in re.findall(r'\d',name_fields[1])))
       if len(name_fields[1])==3 and my_sum ==15:
          return True
       
  else:
    return False


return_value=check_friendly(name_fields)
print ("return value is " + str(return_value))
