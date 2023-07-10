#!/usr/bin/python
#filename: tk_game_overlay.py
#description: create a tk overlay for a full screen application.


import tkinter as tk
import pyautogui
import threading
import time

def press_key(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def on_click(event):
    if event.num == 1:  # Left mouse button
        threading.Thread(target=press_key, args=('w', 120)).start()
    elif event.num == 3:  # Right mouse button
        for _ in range(10):
            threading.Thread(target=press_key, args=('e', 3)).start()
            time.sleep(8)  # 3 seconds for key press + 5 seconds delay

# Create a fullscreen transparent Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.attributes('-alpha', 0.01)  # Set transparency (0.01 is almost fully transparent)
root.configure(bg='white')

# Bind mouse button events to the on_click function
root.bind('<Button-1>', on_click)
root.bind('<Button-3>', on_click)

# Start the Tkinter main loop
root.mainloop()
