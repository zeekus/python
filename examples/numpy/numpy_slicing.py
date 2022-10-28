import numpy as np
array=np.array([2,4,6,8,10])
print(f"1D indexing: display third element in array with 'array[3]' : {array[3]}")

sudoku_game=np.array([[0,0,4,3,0,0,2,0,9],
                     [0,0,5,0,0,9,0,0,1],
                     [0,7,0,0,6,0,0,4,3],
                     [0,0,6,0,0,2,0,8,7],
                     [1,9,0,0,0,7,4,0,0],
                     [0,5,0,0,8,3,0,0,0],
                     [6,0,0,0,0,0,1,0,5],
                     [0,0,3,5,0,8,6,9,0],
                     [0,4,2,9,1,0,3,0,0]])

print(f"print row 3, col 5 - with ref sudoku_game[2,4]: {sudoku_game[2,4]}")

print(f"print the first row aka sudoku_game[0]: {sudoku_game[0]}")

print(f"print the 4th colum of data aka sudoku_game[:,3]: {sudoku_game[:,3]}")

print(f"slice our 1D array {array} and get elements 3-5 aka array[2:4]: {array[2:4]}")

print(f"slice our 2D array:\n{sudoku_game}\nand get elements in the center aka sudoku_game[3:6, 3:6]:\n{sudoku_game[3:6, 3:6]}")

print(f"slice our 2D array:\n{sudoku_game}\nand get every other element (aka step 2) in the center aka sudoku_game[3:6:2, 3:6:2]:\n{sudoku_game[3:6:2, 3:6:2]}")