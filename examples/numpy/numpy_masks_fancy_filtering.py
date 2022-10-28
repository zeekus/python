
import numpy as np
one_to_five = np.arange(1,6)
print(one_to_five)
mask = one_to_five % 2 ==0 #get values divisable by 2 
print(mask)
#fancy indexing is calling the values from the mask
print(f"values from mask capture that are divisable by 2 {one_to_five[mask]}")


#2D fancy indexing
print("2D fancy indexing example with classroom ids and sizes")
classroom_ids_and_sizes = np.array([[1,22], [2,21], [3,27], [4,26] ])
print(classroom_ids_and_sizes)

print("find the classroom ids with an even number of students.")
even_number_of_students=classroom_ids_and_sizes[:,1] % 2 == 0 #mask 
print(classroom_ids_and_sizes[:,0][even_number_of_students]) #get classroom ids with even numbers


# Create an array which contains row data on the largest tree in tree_census
mask = tree_census[tree_census[:, 2] == 51]
#largest_tree_data = tree_census[tree_census[:, 2] == 51]
largest_tree_data = tree_census[mask]
print(largest_tree_data)



# Create an array which contains row data on the largest tree in tree_census
largest_tree_data = tree_census[tree_census[:, 2] == 51]
print(largest_tree_data)

# Slice largest_tree_data to get only the block id
largest_tree_block_id = tree_census[tree_census[:,1]]
print(largest_tree_block_id)

# Create an array which contains row data on all trees with largest_tree_block_id
trees_on_largest_tree_block = tree_census[tree_census[:, 1] == largest_tree_block_id]
print(trees_on_largest_tree_block)

# Create the block_313879 array containing trees on block 313879
block_313879 = tree_census[tree_census[:, 1] == 313879]
print(block_313879)