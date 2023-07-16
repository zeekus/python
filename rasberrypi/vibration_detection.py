from gpiozero import DigitalInputDevice
from time import sleep

# Create a DigitalInputDevice object, assuming the vibration sensor is connected to GPIO pin 4
vibration_sensor = DigitalInputDevice(26)

# Function to handle vibration events
def handle_vibration():
    print("Vibration detected!")
    # Do something when vibration is detected

# Attach event handler to the 'active' event of the vibration sensor
vibration_sensor.when_activated = handle_vibration

# Run the program indefinitely
while True:
    sleep(.1)
    pass

