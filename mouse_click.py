import win32api

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) 

def clickWindow(hwnd, offset):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print('left, top, right, bottom', left, top, right, bottom)
    win32api.SetCursorPos([left + offset, (bottom - top) // 2 + top])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.2)

click(0,0)
