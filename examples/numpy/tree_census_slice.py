# Create an array of the first 100 trunk diameters from tree_census
hundred_diameters = (tree_census[:,2][0:100])
print(hundred_diameters.shape)
print(hundred_diameters)

# Create an array of trunk diameters with even row indices from 50 to 100 inclusive
every_other_diameter = tree_census[50:101:2, 2]
print(every_other_diameter)

# Extract trunk diameters information and sort from smallest to largest
sorted_trunk_diameters = np.sort(tree_census[:,2])
print(sorted_trunk_diameters)