import numpy as np

def determinant(matrix):
    np_matrix = np.array(matrix)
    return round(np.linalg.det(np_matrix))

