#!/usr/bin/python3
#list_windows_open_on_linux_desktop.py

import wmctrl

for w in wmctrl.Window.list():
  print('{w.id:10s} {w.x:4d} {w.y:4d} {w.w:4d} {w.h:4d} {w.wm_name} - {w.wm_class} - {w.wm_window_role}'.format(w=w))
