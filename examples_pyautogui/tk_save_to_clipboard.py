
#filename: tk_save_to_clipboard.py
#description save data to clipboard.

def save_to_clipboard(s):
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(s)
    tk.update()
    tk.destroy()


import tkinter as tk
from tkinter import TclError
tk = tk.Tk()
save_to_clipboard("hello world")
