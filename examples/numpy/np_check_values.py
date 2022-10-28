#filename: np_check_values.py
#description: how to check the values of a multi dimentional array

import numpy as np
m=np.zeros((3,5,9))
print(f"The the dataset has: '{m.size}' entries.")
print(f"The object has a shape of '{m.shape}'.")
count=1
for index,x in np.ndenumerate(m):
    print(f"location: {index},value: {x},entry count: {count}")
    count+=1





