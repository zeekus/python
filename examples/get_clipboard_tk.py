import tkinter as tk
#displays text stored in clipboard to screen

def getClipboardText():
    root = tk.Tk()
    root.withdraw()
    return root.clipboard_get()

myclipboard=getClipboardText()
print(myclipboard)
