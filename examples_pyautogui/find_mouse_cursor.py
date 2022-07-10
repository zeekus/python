#! python3
import pyautogui, sys
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        pix = pyautogui.pixel(x,y)
        r=pix.red
        b=pix.blue
        g=pix.green
        positionStr = 'X:' + str(x).rjust(4) + ',Y:' + str(y).rjust(4) + ' R:' + str(r).rjust(3) + ' B:' + str(b).rjust(3) + ' G:' + str(g).rjust(3)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\n')
