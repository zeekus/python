# Python program to demonstrate
# sys.argv


import sys

print("This is the name of the program:", sys.argv[0])
print("Raw - Argument List:", str(sys.argv))

if len(sys.argv) == 1:
    print("Error: No arguments found.")
else:
    print("Number of arguments:", len(sys.argv) - 1)
    print("Argument List:", str(sys.argv[1:]))