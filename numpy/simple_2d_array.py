#!/usr/bin/python
#filename: simple_2d_array.py
#description: create a simple 2D numpy array
import numpy as np
list_of_lists=([[3,2,5],
              [8,4,9],
              [7,6,1]]) #list of lists
my_numpy_array=np.array(list_of_lists)
print(my_numpy_array)
