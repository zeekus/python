#filename: night_time_nanny.py
#description: The program night_time_nanny.py monitors sound and vibration sensors, logging events and performing actions based on specified thresholds and time ranges.
#The goal of this is to tell my kid to go to sleep when he wakes during the target hours which are 22:00 (10:30PM) to 06:30 (6:30AM)
#the sound sensor is attached to his wall. The vibration sensor is attached to his door. And, there is a usb speaker attached to a raspberrypi pi that gets triggered with espeak.

from gpiozero import Button
import datetime 
import time
import traceback
import os 
import subprocess
import sys

# Setup sensor pins
sound_sensor_pin = 4
vibration_sensor_pin = 26

# Initialize sensor buttons
sound_sensor = Button(sound_sensor_pin, bounce_time=0.01)
vibration_sensor = Button(vibration_sensor_pin, bounce_time=0.01)

# Counter variables for each sensor
sound_sensor_bounce_count = 0
vibration_sensor_bounce_count = 0

# Threshold values for bounce counts
sound_sensor_threshold = 0
vibration_sensor_threshold = 0

# Define start and end times

start_time = "00:00"
end_time = "12:00"

# Split start and end times into hours and minutes
start_hour, start_min = map(int, start_time.split(":"))
end_hour, end_min = map(int, end_time.split(":"))

# handlers area

# Event handler for sound_sensor
def sound_sensor_event(start_hour, start_min, end_hour, end_min):
    global sound_sensor_bounce_count
    try: 
     sound_sensor_bounce_count += 1
     text=(f"Sound Sensor detected an event. Bounce count: {sound_sensor_bounce_count}")
     log_event("raspberrypi",text)
     # Perform specific actions for Sound Sensor
     if (sound_sensor_bounce_count > sound_sensor_threshold):
        text=(f"Sound Sensor theshold exceeded. Bounce count: {sound_sensor_bounce_count}")
        log_event("raspberrypi",text)
        reset_bounce_count()
        threshold_exceeded(start_hour, start_min, end_hour, end_min)
    except Exception as e:
        print(f"Error handling sound sensor event: {e}")

# Event handler for vibration_sensor
def vibration_sensor_event(start_hour, start_min, end_hour, end_min):
    global vibration_sensor_bounce_count
    try: 
     vibration_sensor_bounce_count += 1
     text=(f"Vibration Sensor detected an event. Bounce count: {vibration_sensor_bounce_count}")
     log_event("raspberrypi",text)
     # Perform specific actions for Vibration Sensor
     if (vibration_sensor_bounce_count > vibration_sensor_threshold):
        text=(f"Vibration Sensor theshold exceeded. Bounce count: {sound_sensor_bounce_count}")
        log_event("raspberrypi",text)
        reset_bounce_count()
        threshold_exceeded(start_hour, start_min, end_hour, end_min)
    except Exception as e:
        print(f"Error handling vibration sensor event: {e}")

# Reset bounce counts function
def reset_bounce_count():
    global sound_sensor_bounce_count, vibration_sensor_bounce_count
    counters=f"Reseting Bounce Counts: sounds detected: {sound_sensor_bounce_count},vibrations detected: {vibration_sensor_bounce_count}"
    log_event("raspberrypi",counters)
    sound_sensor_bounce_count = 0
    vibration_sensor_bounce_count = 0

# Function to perform specific action when threshold is exceeded
def threshold_exceeded(start_hour, start_min, end_hour, end_min):

    in_target_time_range = is_within_time_range(start_hour,start_min,end_hour,end_min)

    if in_target_time_range: 
        current_time = datetime.datetime.now().time() #get current time
        end_time = datetime.time(end_hour, end_min)   #gen end hour
        #possibly buggy
        time_difference = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), current_time) #get difference
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds // 60) % 60
        print("Threshold exceeded during sleep time. Go back to bed.")
        sayit_text=f"Be quiet. Go back to bed. There are {hours} hours and {minutes} minutes until morning."
        sayit(sayit_text)
        log_event("raspberrypi", sayit_text)           
    else:
        print("Threshold exceeded during the day.")
        log_event("raspberrypi", f"sayit nothing said. It is outside of {start_hour}:{start_min} PM and {end_hour}:{end_min} AM" )

def adjust_time_for_days(current_datetime,start_hour,start_min,end_hour,end_min):

    # Create datetime objects for start and end times
    start_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(start_hour, start_min, 0))
    end_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(end_hour, end_min, 0))

    # Check if the end time is before the start time if it is increment 1 day 
    if end_datetime < start_datetime:
        # Increment the end day by one
        end_datetime += datetime.timedelta(days=1)
    
    return start_datetime,end_datetime

# Function to check if the current time is within the specified hours
def is_within_time_range(start_hour, start_min, end_hour, end_min):
    # Get the current local time and date
    current_datetime = datetime.datetime.now()

    # Check if the current time is in the specified time zone
    env_tz = os.environ.get('TZ')  # Get the value of the TZ environment variable

    if env_tz and 'EST' in env_tz:
        # Time zone is specified as EST
        est_offset = datetime.timedelta(hours=5)
    else:
        # Time zone is not specified or different from EST
        est_offset = datetime.timedelta(hours=0)

    # Calculate the adjusted time in the specified time zone
    current_datetime_est = current_datetime - est_offset

    text=f"debug: is_within_time_range: current_datetime_est {current_datetime_est}"
    log_event("raspberrypi", text) 

    start_datetime,end_datetime=adjust_time_for_days(current_datetime_est,start_hour,start_min,end_hour,end_min)
 
    if start_datetime <= current_datetime <= end_datetime:
        my_return=True
    else:
        my_return=False

    text=f"debug: is_within_time_range: value returned {my_return}"
    log_event("raspberrypi", text) 
   
    return my_return


#log event function
def log_event(filestring,text):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{filestring}_{current_date}.log"
    log_message = f"{datetime.datetime.now()} - {text}\n"
    print(log_message.rstrip("\n"))

    with open(log_file_name, "a") as log_file:
        log_file.write(log_message)


#sayit sends computer voice through the speakers
def sayit(phrase):
    if os.path.exists("/usr/bin/festival"):
        cmd_talk = "festival --tts"
    elif os.path.exists("/usr/bin/espeak"):
        cmd_talk = "espeak -a 500 -p 1"
    else:
        text=("Sorry, this program will not work without Festival or espeak installed. Please install one.\n")
        log_event("raspberrypi", text)
        return

    cmd_echo = f'echo "{phrase}" | {cmd_talk}'

    text=f"debug: sayit: {cmd_echo}"
    log_event("raspberrypi", text) 

    try:
        status = subprocess.call(cmd_echo, stderr=subprocess.DEVNULL, shell=True)
    except Exception as e:
        traceback.print_exc()

        

#############
#MAIN area
#############

# Assign event handlers to sensors
# sound_sensor.when_pressed = sound_sensor_event
# vibration_sensor.when_pressed = vibration_sensor_event
sound_sensor.when_pressed = lambda: sound_sensor_event(start_hour, start_min, end_hour, end_min)
vibration_sensor.when_pressed = lambda: vibration_sensor_event(start_hour, start_min, end_hour, end_min)


# Attempt to Prevent jitter
sound_sensor.hold_repeat = False
vibration_sensor.hold_repeat = False

# Time Tracking
start_time = datetime.datetime.now().time()
#reset_interval = datetime.timedelta(seconds=5)  # 5 seconds
reset_interval = datetime.timedelta(minutes=1)  # 1 minute

log_event("raspberrypi", f"*** starting monitoring script ***" )

# Keep the program running
while True:
    time.sleep(0.1)
    current_time = datetime.datetime.now().time()

    # Calculate elapsed time as a timedelta object
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), start_time)
    #print(f"debug elapsed time: {elapsed_time}")

    # Reset bounce counts every reset_interval
    if elapsed_time >= reset_interval:
        reset_bounce_count()
        start_time = current_time
