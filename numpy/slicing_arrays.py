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
every_other_diameter = tree_census[50:100 ] #50 elements
every_other_diameter = tree_census[50:100:2,0 ] #25
print(every_other_diameter.shape)
print(every_other_diameter)
