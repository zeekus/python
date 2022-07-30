import pyautogui
import tkinter as tk
import time
import re

def select_and_copy_all():
  pyautogui.keyDown('ctrlleft')
  pyautogui.press('a')
  pyautogui.press('c')
  pyautogui.keyUp('ctrlleft')

def get_game_clipboard():
    select_and_copy_all()
    root = tk.Tk()
    root.withdraw()
    return root.clipboard_get()


print("move your cursor to the game screen.")
print("click on the window you wish to focus on.")
time.sleep(10)

print("grab text from the game screen and save it in the clipboard")
select_and_copy_all()

print("display the text captured")
text=get_game_clipboard()
count=1
list_of_text=re.split(r"[~\r\n]+", text) #convert text string into an array of lines
for line in list_of_text:
    print (line)
