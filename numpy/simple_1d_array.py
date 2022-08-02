#!/usr/bin/python
#filename: simple_1d_array.py
#description: create a simple 1D numpy array
import numpy as np
my_list=[3,2,5,8,4,9,7,6,1] #standard python list/array
np_array=np.array(my_list)  #create a numpy array
print("The array is ",str(np_array))
print("The object type is ",type(np_array))