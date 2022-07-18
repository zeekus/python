#! python3
import pyautogui, sys

x,y = pyautogui.position()
print( 'X:' + str(x).rjust(4) + ',Y:' + str(y).rjust(4) )
print('\n')
