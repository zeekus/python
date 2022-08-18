import tkinter as tk
import sys
#displays text stored in clipboard to screen

def getClipboardText():
    root = tk.Tk()
    #root.withdraw()
    try: 
      myclip=root.clipboard_get()
    except tk.TclError:
      myclip=None
    return myclip

def clear_clipboard():
    root = tk.Tk()
    root.clipboard_clear()
    root.destroy()

def append_something():
    root = tk.Tk()
    root.clipboard_append("123 test")

#append_something()
myclip=getClipboardText()

clear_clipboard()
if myclip is not None:
    print("clip board data reads: '" + myclip + "'")
else:
  print("empty clipboard")
