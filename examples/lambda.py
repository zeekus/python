x=[1, 2, 3, -1]

sum(filter(lambda y: y >0,x)) #sum of numbers larger than 0
#6

len(filter(lambda y: y >0,x)) #length of array after we filter out the values less than 0
#3

#>>> b=(filter(lambda y: y >0,x))
#>>> b
#[1, 2, 3]


