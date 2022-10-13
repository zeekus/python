
#filename: split_text_example.py
#description: demonstrates how to parse a string using split

string="1 2 3 4 5 6 7 8 9 10"
myarray=string.split(" ")
print (str(myarray))
myarray2=string.split(" ")[:-2] #drop last 2 fields
print (str(myarray2))
myarray3=(string.split(" ")[+3:-3]) #range from array field 3 to -3
print (str(myarray3))
myarray4=(string.split(" ")[-8:]) #last 8 in array
print (str(myarray4))
string1=(string.split(" ")[1]) #only the string value from the 2nd element in the array
print (string1)
print((string.split(" ")[:3]))# first three elements printing array as a string