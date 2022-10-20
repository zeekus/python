#!/usr/bin/python3
#filename: change_focust_to_each_object.py

import wmctrl
import time
import os 

#page=("GitHub Authentication - Sign In — Mozilla Firefox - Navigator.firefox - browser")

for w in wmctrl.Window.list():
  print('{w.id:10s} {w.x:4d} {w.y:4d} {w.w:4d} {w.h:4d} {w.wm_name} - {w.wm_class} - {w.wm_window_role}'.format(w=w))
  #print('1:{w.id:10s} 2:{w.x:4d} 3:{w.y:4d} 4:{w.w:4d} 5:{w.h:4d} 6:{w.wm_name} - 7:{w.wm_class} - 8.{w.wm_window_role}'.format(w=w))
  os.system('wmctrl -id -a %s' % (w.id))
  #wmctrl.Window.activate(str(w.id)) #not working not sure why
  time.sleep(2)
  
