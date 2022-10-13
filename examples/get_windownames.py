import pyautogui
windownames=pyautogui.getAllWindows()
for window in windownames:
    print(window.title)
