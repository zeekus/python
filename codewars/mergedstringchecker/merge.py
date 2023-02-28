def is_merge(s, part1, part2):
   print (s)
   print (part1,part2)
   myparts=sortString(part1+part2)
   s=sortString(s)
   print("s:",str(s)) 
   print("parts:",str(myparts))
   if s==myparts and len(s)==len(myparts):
    return True
   else: 
    return False
       
def sortString(str):
    return ''.join(sorted(str))
     