import time
import pyautogui
import random

print("click on game screen")
time.sleep(10)

while True: 
    print("pressing v")
    pyautogui.typewrite('v') #press v for scanner
    random_delay=random.randint(1,7)
    random_delay= random_delay + random.randint(0,100)*.01
    print("sleeping for " + str(round(random_delay,2)) + " seconds")
    time.sleep(random_delay)

