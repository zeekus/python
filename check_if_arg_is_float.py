import sys

def help_message():
    print("help_message called")
    print("This program checks if a string is a float.")
    print(f"Usage: python {sys.argv[0]} <string>")
    print(f"Example: python {sys.argv[0]}  3.14")

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if "--help" in sys.argv:
    help_message()
else:
    if len(sys.argv) != 2:
        print("Error: Please provide one string argument.")
        help_message()
    else:
        if is_float(sys.argv[1]):
            print(f"{sys.argv[1]} is a float.")
        else:
            print(f"{sys.argv[1]} is a not a float.")
