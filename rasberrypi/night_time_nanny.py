#filename: night_time_nanny.py
#description: The program night_time_nanny.py monitors sound and vibration sensors, logging events and performing actions based on specified thresholds and time ranges.
#The goal of this is to tell my kid to go to sleep when he wakes during the target hours which are 22:00 (10PM) to 07:00 (7AM)
#the sound sensor is attached to his wall. The vibration sensor is attached to his door. And, there is a usb speaker attached to a rasberry pi that gets triggered with espeak.

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
sound_sensor_threshold = 3
vibration_sensor_threshold = 2

# handlers area

# Event handler for sound_sensor
def sound_sensor_event():
    global sound_sensor_bounce_count
    try: 
     sound_sensor_bounce_count += 1
     text=(f"Sound Sensor detected an event. Bounce count: {sound_sensor_bounce_count}")
     log_event("sound",text)
     # Perform specific actions for Sound Sensor
     if (vibration_sensor_bounce_count > vibration_sensor_threshold) and (sound_sensor_bounce_count > sound_sensor_threshold):
        reset_bounce_count()
        threshold_exceeded()
    except Exception as e:
        print(f"Error handling sound sensor event: {e}")

# Event handler for vibration_sensor
def vibration_sensor_event():
    global vibration_sensor_bounce_count
    try: 
     vibration_sensor_bounce_count += 1
     text=(f"Vibration Sensor detected an event. Bounce count: {vibration_sensor_bounce_count}")
     log_event("vibration",text)
     # Perform specific actions for Vibration Sensor
     if (vibration_sensor_bounce_count > vibration_sensor_threshold) and (sound_sensor_bounce_count > sound_sensor_threshold):
        reset_bounce_count()
        threshold_exceeded()
    except Exception as e:
        print(f"Error handling vibration sensor event: {e}")

# Reset bounce counts function
def reset_bounce_count():
    global sound_sensor_bounce_count, vibration_sensor_bounce_count
    counters=f"sounds detected: {sound_sensor_bounce_count},vibrations detected: {vibration_sensor_bounce_count}"
    log_event("reseting_counters",counters)
    print(f"Bounce counters reset - {counters}")
    sound_sensor_bounce_count = 0
    vibration_sensor_bounce_count = 0

# Function to perform specific action when threshold is exceeded
def threshold_exceeded():

    if_result_is_true = is_within_time_range(start_hour=22, end_hour=7)

    if if_result_is_true: 
        print("Threshold exceeded during sleep time. Go back to bed.")
        sayit("It is sleep time. Go back to bed.")
        log_event("sayit","It is sleep time. Go back to bed.")
    else:
        print("Threshold exceeded during the day.")

#log event function
def log_event(sensor_name,text):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{sensor_name}_{current_date}.log"
    log_message = f"{datetime.datetime.now()} - {sensor_name} {text}\n"
    print(log_message.rstrip("\n"))

    with open(log_file_name, "a") as log_file:
        log_file.write(log_message)

# Function to check if the current time is within the specified hours
def is_within_time_range(start_hour, end_hour):
    # Get the current local time
    current_time = datetime.datetime.now().time()

    # Check if the current time is in the specified time zone
    env_tz = os.environ.get('TZ')  # Get the value of the TZ environment variable

    if env_tz and 'EST' in env_tz:
        # Time zone is specified as EST
        est_offset = datetime.timedelta(hours=5)
    else:
        # Time zone is not specified or different from EST
        est_offset = datetime.timedelta(hours=0)

    # Calculate the adjusted time in the specified time zone
    current_datetime = datetime.datetime.now()
    current_datetime_est = current_datetime - est_offset

    # Check if the current time is between the start and end times in the specified time zone
    print(f"debug: current_time is {current_time}")
    print(f"debug: current_datetime_est is {current_datetime_est.time()}")

    start_time = datetime.time(start_hour, 0, 0)
    end_time = datetime.time(end_hour, 0, 0)

    if start_time <= current_time <= end_time:
        return True
    return False

#sayit sends computer voice through the speakers
def sayit(phrase):
    cmd_echo = f"echo {phrase}"

    if os.path.exists("/usr/bin/festival"):
        cmd_talk = "festival --tts"
        #errors get chatty so I am sending them to devnull
        try:
            status = subprocess.call(cmd_echo + "|" + cmd_talk, stderr=subprocess.DEVNULL, shell=True)
        except Exception as e:
            traceback.print_exc()
            print(f"Error executing festival command: {e}")
    elif os.path.exists("/usr/bin/espeak"):
        cmd_talk = "espeak -a 500 -p 1 "
        try:
            status = subprocess.call(cmd_echo + "|" + cmd_talk, stderr=subprocess.DEVNULL, shell=True)
        except Exception as e:
            traceback.print_exc()
            print(f"Error executing espeak command: {e}")
    else:
        print("Sorry, this program will not work without Festival or espeak installed. Please install one.\n")
        sys.exit(1)

        


#############
#MAIN area
#############

# Assign event handlers to sensors
sound_sensor.when_pressed = sound_sensor_event
vibration_sensor.when_pressed = vibration_sensor_event

# Attempt to Prevent jitter
sound_sensor.hold_repeat = False
vibration_sensor.hold_repeat = False

# Time Tracking
start_time = datetime.datetime.now().time()
#reset_interval = datetime.timedelta(seconds=5)  # 5 seconds
reset_interval = datetime.timedelta(minutes=1)  # 1 minute

print("starting monitoring.")

# Keep the program running
while True:
    time.sleep(0.1)
    current_time = datetime.datetime.now().time()

    # Calculate elapsed time as a timedelta object
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), start_time)

    #print(f"debug elapsed time: {elapsed_time}")

    # Reset bounce counts every reset_interval
    if elapsed_time >= reset_interval:
        formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"reset {formatted_time}")
        reset_bounce_count()
        start_time = current_time
