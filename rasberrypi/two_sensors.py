from gpiozero import Button
from time import sleep

#Setup sensor pins
sound_sensor_pin=4
vibration_sensor_pin=26

#intialize sensor buttons
sound_sensor = Button(sound_sensor_pin,bounce_time=0.05)
vibration_sensor = Button(vibration_sensor_pin,bounce_time=0.05)

#Event handler for sound_sensor
def vibration_sensor_event():
    print("Vibration Sensor detected an event.")
    # Preform specific actions for Vibration Sensor

def sound_sensor_event():
    print("Sound Sensor detected an event.")
    # Preform specific actions for Sound Sensor

# Assign event handlers to sensors
sound_sensor.when_pressed = sound_sensor_event
vibration_sensor.when_pressed = vibration_sensor_event

#prevent jitter ? 
sound_sensor.hold_repeat=False
vibration_sensor.hold_repeat=False

#Keep the program running
while True:
    sleep(0.1)

