import numpy as np

# Select all rows of block ID data from the second column
block_ids = np.array(tree_census)
block_id_slice=(block_ids[:,1])

# Print the first five block_ids
print (block_id_slice[0:5])
print (block_id_slice[:5])

# Select all rows of block ID data from the second column
block_ids = tree_census[:, 1]

# Select the tenth block ID from block_ids
tenth_block_id = block_ids[10]
print(tenth_block_id)

# Select all rows of block ID data from the second column
block_ids = tree_census[:, 1]

# Select five block IDs from block_ids starting with the tenth ID
block_id_slice = block_ids[10:15]
print(block_id_slice)


# Create an array of the first 100 trunk diameters from tree_census
hundred_diameters = tree_census[:,2]
hundred_diameters = hundred_diameters[:100]
print(hundred_diameters.shape)
print(hundred_diameters)

# Create an array of trunk diameters with even row indices from 50 to 100 inclusive
every_other_diameter = tree_census[50:101 ] #50 elements
every_other_diameter = tree_census[50:101:2, 2] #25 
print(every_other_diameter.shape)
print(every_other_diameter)


# Extract trunk diameters information and sort from smallest to largest
sorted_trunk_diameters = np.sort(tree_census[:, 2])
print(sorted_trunk_diameters)

#filters in numpy
np.where()
one_to_five=np.arange(1,6)
mask = one_to_five % 2==0
one_to_five[mask]


#fancy filtering
array([[1,22],
       [2,21],
       [3,27],
       [4,26]])

np.where(array[:,1] % 2 ) #get array locations where field 2 is div by 2 or even
#(array([0,3]),) #result is a truple

#find and replace
np.where(sudoku_game ==0, "", sudoku_game) #find and replace 0s with ""

# Create an array which contains row data on the largest tree in tree_census
largest_tree_data = tree_census[tree_census[:, 2] == 51]
print(largest_tree_data)