import numpy as np
tree_census=np.zeros((10,4)) #10 lines of 4 zerros
new_trees=np.zeros((4,))     #one line of 4 zerors

print(tree_census)
print(new_trees)

new_trees=new_trees.reshape(1,4)
print(tree_census.shape,new_trees.shape)


# Add rows to tree_census which contain data for the new trees
updated_tree_census = np.concatenate((tree_census,new_trees))
print(updated_tree_census)
