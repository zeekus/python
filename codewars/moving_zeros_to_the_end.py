def move_zeros(my_array):
   

  new_array=[]
  zero=[]
  for x in my_array:
     if x == 0: 
       new_array.pop
       zero.push(str(0))
     else:
       new_array.append(str(x))

  print("nw" + str(new_array))  
  print("zero" + str(zero))
  new_array = new_array + zero


  return new_array
  #move_zeros([1, 0, 1, 2, 0, 1, 3]) # returns [1, 1, 2, 1, 3, 0, 0]


my_array=[1, 0, 1, 2, 0, 1, 3]
new_array=move_zeros(str(my_array))
print(new_array)
