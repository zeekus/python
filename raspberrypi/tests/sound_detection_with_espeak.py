from gpiozero import DigitalInputDevice
from time import sleep
import os
import subprocess

# Create a DigitalInputDevice object, assuming the sound sensor is connected to GPIO pin 4
sound_sensor = DigitalInputDevice(4)

# Function to handle sound events
def handle_sound():
    print("Sound detected!")
    sayit("sound detected")
    # Do something when sound is detected

def  sayit(phrase):
  cmd_echo = f"echo {phrase}"

  if os.path.exists("/usr/bin/festival"):
    #if festival use it
    cmd_talk="festival --tts"
    status = subprocess.call(cmd_echo + "|" + cmd_talk , stderr=subprocess.DEVNULL, shell=True)
  elif os.path.exists("/usr/bin/espeak"):
    cmd_talk="espeak -a 500 -p 1 "
    status = subprocess.call(cmd_echo + "|" + cmd_talk , stderr=subprocess.DEVNULL, shell=True)
  else:
     print ("sorry this program will not work without festival or espeak. Please install one.\n")
     sys.exit(1)


# Attach event handler to the 'active' event of the sound sensor
sound_sensor.when_activated = handle_sound

# Run the program indefinitely
while True:
    sleep(.1)
    pass

