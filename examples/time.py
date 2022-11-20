#description: converting time time can be stored in string format, turple format, or seconds. This converts them into diffent datatypes
#filename: time.py

import time
import os
#source: https://docs.python.org/3/library/time.html#function

mytimestr="2022.11.19 15:36:48" #standard string time found in the game logs

os.environ['TZ']='EST'
print(f"0. timezone is set for {os.environ['TZ']} in the os environment")
#set timezone to gmt
os.environ['TZ']='gmt'
time.tzset()
print(f"1. timezone is set for {os.environ['TZ']} in the os environment")

if time.localtime() == time.gmtime():
    print (f"2. match found: \n ..local time:{time.localtime()} \n ..gmt time  :{time.gmtime()}")
else:
    print ("2. no match found {time.localtime()} ne {time.gmtime()}")
timenow=time.time() #get time in seconds for current timezone
gmt=time.gmtime()   #gets time in a tuple in gmt format
print(f"3. gmt tuple data type: {type(gmt)}")
print(f"4. gmt time: {gmt}")
print("5. convert turple to string using time.strftime")
print(f"5. time.gmtime() has type: {type(time.gmtime())}")
game_style_time=time.strftime("%Y.%m.%d %H:%M:%S", time.gmtime())
print(f"5. game_style_type has type: {type(game_style_time)}")
print(f"5. Game Style Time: {game_style_time}")

t=time.time()#get time in secs
print(f"6. time in secs: {t}")
str_time_now=time.ctime(t)#convert time in secs to string
print(f"7. time as string default format: {str_time_now}")
turple_time=time.strptime(str_time_now, "%a %b %d %H:%M:%S %Y" )
str_time_now=(time.strftime("%Y.%m.%d %H:%M:%S",turple_time))
print(f"8. current time utc game style: {str_time_now}")
