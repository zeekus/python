#filename: read_file.py
# Open a file: file
file = open ('moby_dick.txt', 'r', encoding="utf-8")

# Print it
print(file.read())

# Check whether file is closed
print(file.closed)

# Close file
file.close()

# Check whether file is closed
print(file.closed)
