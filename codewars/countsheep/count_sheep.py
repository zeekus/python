#take an array of data and count the true values discard everything else

def count_sheeps(sheep):
  count =0
  for x in sheep:
    if x==True: 
        count=count+1
  return count

sheep=[ True, False, True, 'nil', 'nothing', True, False, True]
mycount=count_sheeps(sheep)
print(str(mycount) + ": Sheep")