import subprocess
import re
import sys
import pyautogui
import cv2 as cv
import random

def get_session_info(target_string):
    # Print debug message
    print(f"Debug: get_session_info called with target string '{target_string}'")
    
    # Run wmctrl command and split output into lines
    try:
        output = subprocess.check_output(["wmctrl", "-p", "-G", "-l"]).decode('utf-8').split('\n')
    except subprocess.CalledProcessError:
        print("Error: Failed to run wmctrl command.")
        sys.exit(1)
    
    # Iterate over lines and extract fields
    for line in output:
        if target_string in line:
            fields = re.split(r'\s+', line)
            if len(fields) < 7:
                print("Error: Insufficient fields in wmctrl output.")
                sys.exit(1)
            id_field = fields[0]
            x, y, x1, y1 = fields[3:7]
            
            # Return fields as a tuple
            return id_field, x, y, x1, y1
    
    # If session ID not found, exit with error
    print("Error: Session ID not found.")
    sys.exit(1)


def change_session(session_id):
    try:
        out = subprocess.Popen(('wmctrl', '-id', '-a', session_id))  # change the screen using session_id
    except subprocess.CalledProcessError:
        print("Error: Failed to change session.")
        sys.exit(1)



id,x,y,x1,y1 = get_session_info("VE -")
print(f"id is '{id}' x is '{x}' and y is '{y}' x1 is '{x1}' and y1 is '{y1}'")

change_session(id)



# Generate random x and y coordinates within the range of 30-100
try:
    my_x = random.randint(30, 100) + int(x)
    my_y = random.randint(30, 100) + int(y)
    pyautogui.click(my_x,my_y)
except ValueError:
    print("Error: Invalid coordinates for randomization.")
    sys.exit(1)


