from gpiozero import Button
from datetime import datetime
from time import sleep, time
import os 
import subprocess

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
    if is_within_time_range(23, 6):
        print("Threshold exceeded during sleep time. Go back to bed.")
        sayit("It is sleep time. Go back to bed.")
        #reset_bounce_count
        # Add code here to call the speak function or perform desired actions
    else:
        print("Threshold exceeded outside of sleep time. This is okay.")
        sayit("why are you making so much noise ?")
        #reset_bounce_count

# Event handler for sound_sensor
def sound_sensor_event():
    global sound_sensor_bounce_count
    sound_sensor_bounce_count += 1
    print(f"Sound Sensor detected an event. Bounce count: {sound_sensor_bounce_count}")
    # Perform specific actions for Sound Sensor
    if (vibration_sensor_bounce_count > vibration_sensor_threshold) and (sound_sensor_bounce_count > sound_sensor_threshold):
        threshold_exceeded()

# Event handler for vibration_sensor
def vibration_sensor_event():
    global vibration_sensor_bounce_count
    vibration_sensor_bounce_count += 1
    print(f"Vibration Sensor detected an event. Bounce count: {vibration_sensor_bounce_count}")
    # Perform specific actions for Vibration Sensor
    if (vibration_sensor_bounce_count > vibration_sensor_threshold) and (sound_sensor_bounce_count > sound_sensor_threshold):
        threshold_exceeded()

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

def sayit(phrase):
    cmd_echo = f"echo {phrase}"

    if os.path.exists("/usr/bin/festival"):
        cmd_talk="festival --tts"
        status = subprocess.call(cmd_echo + "|" + cmd_talk, stderr=subprocess.DEVNULL, shell=True)
    elif os.path.exists("/usr/bin/espeak"):
        cmd_talk="espeak -a 500 -p 1 "
        status = subprocess.call(cmd_echo + "|" + cmd_talk, stderr=subprocess.DEVNULL, shell=True)
    else:
        print ("sorry this program will not work without Festival or espeak isnstalled. Please install one.\n")
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
