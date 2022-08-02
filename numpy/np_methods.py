import numpy as np


#np.zeros()
#np.random.random()
#np.arange()

print(np.zeros((5,3))) #creates an array full of errors.
#5 rows or lines deep
#3 columns wide

print(np.random.random((2,4))) #creates random numbers 
#2 lines deep
#4 columns

print(np.arange(-3,4))

print(np.arange(4))

print(np.arange(-33, 0, 3)) #last value is step

#array attribute
#.shape

#array methods
#.flatten()
#.reshape()

# Create the game_and_solution 3D array from two 2d arrays.
#game_and_solution = np.array([sudoku_game, sudoku_solution])

# Print game_and_solution
#print(game_and_solution) 