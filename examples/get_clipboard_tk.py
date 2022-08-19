import tkinter as tk
import sys
#displays text stored in clipboard to screen

def getClipboardText():
    cb = tk.Tk()
    try: 
      myclip=cb.clipboard_get()
    except tk.TclError:
      myclip=None
    return myclip

def clear_clipboard():
    cb = tk.Tk()
    cb.clipboard_clear()
    cb.destroy()

def append_something():
    cb = tk.Tk()
    cb.clipboard_append("123 test")

############
#main
############
#append_something()       #append something to clpboard
myclip=getClipboardText() #get active clipboard
clear_clipboard()         #clear clipboard

if myclip is not None:
    print("clip board data reads: '" + myclip + "'")
else:
  print("empty clipboard")
