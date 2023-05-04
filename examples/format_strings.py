#description: string printing examples in python
#filename: format_strings.py

a="String1"


#format example
print("a simple string using format")
string_in_string= "Simple Curly base example: My string is \'{}\'.".format(a)
print (string_in_string)

b=15
#curly brace example
string_in_string2= "Curly brace example2: My string is \'{}\' my number is \'{}\'.".format(a,b)
print (string_in_string2)

#number print example with 4 places
print ("Formatted digit example: number formated with 4 digits {:04d} is here.".format(b))

#number print example with 4 decimal places
print ("Formatted float number example: number formated with 4 digits {:04.4f} is here.".format(b))

#fstrings
string_in_string3= f"F-string Example: My string is {a} my number is {b}."
print (string_in_string3)

#old string example
string_in_string4= "Legacy string example: My string is %s my number is %d." % (a,b)
print (string_in_string4)




