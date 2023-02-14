import pyautogui
pyautogui.sleep(10)
x1,y1,w,h=pyautogui.locateOnScreen("_bu_yellow_gate1.png",confidence=0.8)
print(f"returned: x:{x1},y:{y1},w:{w},h:{h}")
pyautogui.moveTo(x1,y1)
x2=x1+w
y2=y1+h
print(f"start: x:{x1},y:{y1}")
print(f"stop : x:{x2},y:{y2}")

for x in range( x1,x2,2):
  for y in range(y1,y2,2):   
     r,g,b=pyautogui.pixel(x,y)
     pyautogui.moveTo(x,y)
     print(f"checking {x},{y}: rgb is {r},{b},{g}")
     if r>=130 and r<200 and g>=120 and g<200 and g<15:
         print(f"{x,y}: rgb is {r},{b},{g}: yellow")
         break
