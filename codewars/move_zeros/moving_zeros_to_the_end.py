def move_zeros(x):
   myzeros=list(filter(lambda a: a==0, x)) #list of 0 
   mynum=list(filter(lambda a: a!=0, x))   #list of numbers without 0
   return mynum+myzeros                    #return the lists