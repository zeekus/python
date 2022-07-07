#!/usr/bin/python3
#filename: windows_idle_time_monitor.py
#description: monitor idle time windows
#windows win32 specific

#from shutil import move
import win32gui
import win32api
import win32con
import inspect #look at objects
import time
import numpy as np
import random 
#python3 -m pip install win32gui 
#python3 -m pip install win-api #win32api 
#python3 -m pip install pypiwin32 #win32con




def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    source: https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/
    '''
    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))

        #print (move_x,move_y)
        win32api.SetCursorPos((move_x,move_y))
        
        time.sleep(0.01) #can we make this delay increase as time passes ? 
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            #move_mouse(current_x:=move_x,current_y:=move_y)
            win32api.SetCursorPos((move_x,move_y))
    return current_x,current_y

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
idle_time=0
wait=30

while True: 
    x,y=pointer_location()
    time.sleep(30)
    x1,y1=pointer_location()
    if x==x1 and y==y1:
        #no movement
        idle_time=wait+idle_time
        dest_x=random.randrange(0,int(w),1)
        dest_y=random.randrange(0,int(h),1)
        print ("idle_time is " + str(idle_time) )
        print ("moving mouse to location " + str(dest_x) + "," + str(dest_y ))
        wind_mouse(x, y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda dest_x,dest_y: None)
        left_click(dest_x,dest_y)
        

