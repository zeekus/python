import pyautogui, time

def compare_pointer_position(last_x,last_y):
  x,y = pyautogui.position()
  print( 'X:' + str(x).rjust(4) + ',Y:' + str(y).rjust(4) )
  if last_x == x and last_y ==y:
    #no movement detected 
    print("no mouse movement since last check.")
  else:
    #movement
    print("we detected mouse movement.")

while True:
    x,y = pyautogui.position()
    time.sleep(5)
    compare_pointer_position(x,y)
