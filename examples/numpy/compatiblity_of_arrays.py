import numpy as np
tree_census=np.zeros((1000,4))
new_trees=np.zeros((2,4))

# Print the shapes of tree_census and new_trees
print(tree_census.shape, new_trees.shape)

# Add rows to tree_census which contain data for the new trees
updated_tree_census = np.concatenate((tree_census,new_trees))
print(updated_tree_census)


