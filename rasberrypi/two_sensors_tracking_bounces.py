from gpiozero import Button
import time

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
    print("Threshold exceeded. Go back to bed.")
    # Add code here to call the speak function or perform desired actions

# Event handler for sound_sensor
def sound_sensor_event():
    global sound_sensor_bounce_count
    sound_sensor_bounce_count += 1
    print(f"Sound Sensor detected an event. Bounce count: {sound_sensor_bounce_count}")
    # Perform specific actions for Sound Sensor

# Event handler for vibration_sensor
def vibration_sensor_event():
    global vibration_sensor_bounce_count
    vibration_sensor_bounce_count += 1
    print(f"Vibration Sensor detected an event. Bounce count: {vibration_sensor_bounce_count}")
    # Perform specific actions for Vibration Sensor

def reset_bounce_count():
    global sound_sensor_bounce_count, vibration_sensor_bounce_count
    sound_sensor_bounce_count = 0
    vibration_sensor_bounce_count = 0 
    print("Bounce counters reset.")

# Assign event handlers to sensors
sound_sensor.when_pressed = sound_sensor_event
vibration_sensor.when_pressed = vibration_sensor_event

# Prevent jitter
sound_sensor.hold_repeat = False
vibration_sensor.hold_repeat = False

#Time Tracking
start_time = time.time()
reset_interval = 5 * 60 # 5 minutes

# Keep the program running
while True: 
    time.sleep(0.1)
    elapsed_time = time() - start_time
    # Reset bounce counts every 5 minutes
    if elapsed_time >= reset_interval:
        reset_bounce_count()
        start_time = time()