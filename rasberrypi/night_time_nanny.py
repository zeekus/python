from gpiozero import Button
from datetime import datetime
from time import sleep, time
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
sound_sensor_threshold = 10
vibration_sensor_threshold = 10

# Function to perform specific action when threshold is exceeded
def threshold_exceeded():
    print("Threshold exceeded during sleep time. Go back to bed.")
    sayit("It is sleep time. Go back to bed.")
    log_event("sayit","It is sleep time. Go back to bed.")


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

def log_event(sensor_name,text):
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{sensor_name}_{current_date}.log"
    log_message = f"{datetime.now()} - {sensor_name} {text}\n"
    print(log_message.rstrip("\n"))

    with open(log_file_name, "a") as log_file:
        log_file.write(log_message)


# Assign event handlers to sensors
sound_sensor.when_pressed = sound_sensor_event
vibration_sensor.when_pressed = vibration_sensor_event

# Prevent jitter
sound_sensor.hold_repeat = False
vibration_sensor.hold_repeat = False

# Function to check if the current time is within the specified hours
def is_within_time_range(start_hour, end_hour):
    now = datetime.now().time()
    start_time = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0).time()
    end_time = datetime.now().replace(hour=end_hour, minute=0, second=0, microsecond=0).time()

    if start_time <= now <= end_time:
        return True
    return False

# Reset bounce counts function
def reset_bounce_count():
    global sound_sensor_bounce_count, vibration_sensor_bounce_count
    sound_sensor_bounce_count = 0
    vibration_sensor_bounce_count = 0
    print("Bounce counters reset.")
    log_event("reseting_counters","")

def sayit(phrase):
    cmd_echo = f"echo {phrase}"

    if os.path.exists("/usr/bin/festival"):
        cmd_talk = "festival --tts"
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

# Time Tracking
start_time = time()
reset_interval = 5 * 60  # 5 minutes

# Keep the program running
while True:
    sleep(0.1)
    elapsed_time = time() - start_time

    # Reset bounce counts every 5 minutes
    if elapsed_time >= reset_interval:
        reset_bounce_count()
        start_time = time()
