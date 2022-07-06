#!/usr/bin/python3
#filename: screen_interaction.py
#description: basic screen interaction python.

import win32gui
import win32api
import win32con
import inspect #look at objects
import time
#python3 -m pip install win32gui 
#python3 -m pip install win-api #win32api 
#python3 -m pip install pypiwin32 #win32con

def get_screensize():
    w=win32api.GetSystemMetrics(0) #width
    h=win32api.GetSystemMetrics(1) #height
    return w,h

def pointer_location():
    x,y=win32api.GetCursorPos()
    return x,y

def pixel_color(x,y):
    color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x , y)
    return (color) #RGB int

def rgbint2rgbtuple(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return (red, green, blue)

def left_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) 
    time.sleep(0.2)

def right_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0) 
    time.sleep(0.2)

def clickWindow(hwnd, offset):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print('left, top, right, bottom', left, top, right, bottom)
    win32api.SetCursorPos([left + offset, (bottom - top) // 2 + top])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.2)


w,h=get_screensize()
print('Screensize - Width:' + str(w) + ',Height:' + str(h) )

x,y=pointer_location()
print ("current x,y location is ", str((x,y)))
color=pixel_color(x,y)
print ("pixel int color is '" + str(color) +"'")
print ("pixel hex color is '" + hex(color) +"'")
print("pixel r,g,b, truple color is " + str(rgbint2rgbtuple(color)) )
x1=0
y1=0
print ("moving mouse to location " + str(x1) + "," + str(y1)) 

left_click(x1,y1)

# for name, obj in inspect.getmembers(win32api):
#     print(str(name))

