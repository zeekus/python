# Import the tkinter library
from tkinter import *

# Instance of tkinter canvas
win = Tk()
win.geometry("700x250")
win.title("Data from Clipboard")

# Get the data from the clipboard
win.clipboard_append("this is appended to the clipboard")
cliptext = win.clipboard_get()
win.clipboard_clear() #clear clipboard

# Label to print clipboard text
lab=Label(win, text = cliptext, font=("Calibri",15,"bold"))
lab.pack(padx=20, pady=50)

# Run the mainloop
win.mainloop()
