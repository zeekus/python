#filename: tk_clear_clipboard.py
#description if clipboard is not empty clear it.

import tkinter as tk
from tkinter import TclError

def is_clipboard_empty():
    try:
      r.selection_get(selection="CLIPBOARD")
    except TclError: 
        return True #clipboard empty
    return False #clipboard not empty


r=tk.Tk()
empty=is_clipboard_empty()
print("Is clipboard empty:" + str(empty))

if empty==False:
  r.withdraw() #hide tk interface
  r.clipboard_clear() #clear clipboard
  r.update() #force update
  r.destroy() #destroy session ?
