import numpy as np

classroom_ids_and_sizes = np.array([[1,22], [2,21], [3,27], [4,26] ])
print("classroom ids with a class size with an even number")
indices=np.where(classroom_ids_and_sizes[:,1] % 2 ==0) #gets indices of trues
print(indices)
print(np.array(indices))


print("sudoku game:")
sudoku_game=np.array([[0,0,4,3,0,0,2,0,9],
                     [0,0,5,0,0,9,0,0,1],
                     [0,7,0,0,6,0,0,4,3],
                     [0,0,6,0,0,2,0,8,7],
                     [1,9,0,0,0,7,4,0,0],
                     [0,5,0,0,8,3,0,0,0],
                     [6,0,0,0,0,0,1,0,5],
                     [0,0,3,5,0,8,6,9,0],
                     [0,4,2,9,1,0,3,0,0]])

row_indices,col_indices = np.where(sudoku_game==0)
print(row_indices)
print(col_indices)


#find and replace 0 with empty strings with np.where
no_zeros=np.where(sudoku_game==0,"",sudoku_game)

print(no_zeros)


# Create an array of row_indices for trees on block 313879
row_indices = np.where(tree_census[:, 1] == 313879)

# Create an array which only contains data for trees on block 313879
block_313879 = tree_census[row_indices]
print(block_313879)

# Create and print a 1D array of tree and stump diameters
trunk_stump_diameters = np.where(tree_census[:, 2] == 0, tree_census[:, 3], tree_census[:, 2])
print(trunk_stump_diameters)