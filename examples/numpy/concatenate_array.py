import numpy as np

classroom_ids_and_sizes = np.array([[1,22], [2,21], [3,27], [4,26] ])
print(f"classroom_ids_and_sizes array looks like:\n {classroom_ids_and_sizes}")
new_classrooms = np.array([[5,30],[6,17]])
print(f"new classrooms array looks like:\n {new_classrooms}")
new_array=np.concatenate((classroom_ids_and_sizes,new_classrooms))

print(f"concatenated array looks like:\n {new_array}")

#add more fields to existing data
grade_levels_and_teachers=np.array([[1,"James"],[1,"George"], [3,"Amy"], [4,"Sims"]])
new_data=np.concatenate((classroom_ids_and_sizes, grade_levels_and_teachers), axis=1)
print(f"{new_data}")