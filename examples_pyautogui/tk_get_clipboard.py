import tkinter as tk

def check_clipboard():
    r = tk.Tk()
    r.withdraw()
    try:
        print("clipboard has data")
        return r.selection_get(selection="CLIPBOARD")
        #return r.clipboard_get() #same as above
    except tk.TclError:
        print("clipboard is empty")
        return None
    finally:
        r.destroy()


myclip=check_clipboard()
print("my clip: " + myclip)
