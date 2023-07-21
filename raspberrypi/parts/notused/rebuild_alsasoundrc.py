import subprocess
import os
import re
import sys
def get_usb_devices():
    #remove potentially erronous asoundrc files
    asoundrc_path = os.path.join(os.environ['HOME'], '.asoundrc')
    if os.path.exists(asoundrc_path):
      os.remove(asoundrc_path)
    # Run the command and capture the output from aplay to list sound devices
    output = subprocess.check_output(['aplay', '-l']).decode()
    devices = [line for line in output.split('\n') if 'USB' in line] #devices with a USB indicator for my speaker
    card_number = devices[0].split()[1][:-1] #get card number from the device line with USB in it
    return card_number
def setup_asoundrc():
    # Scan for ALSA devices
    devices = get_usb_devices()

    # Set up .asoundrc file
    asoundrc_path = os.path.join(os.environ['HOME'], '.asoundrc')
    with open(asoundrc_path, 'w') as f:
        f.write('pcm.!default {\n')
        f.write('  type hw\n')
        f.write(f'  card {devices[0]}\n')
        f.write('}\n')
        f.write('ctl.!default {\n')
        f.write('  type hw\n')
        f.write(f'  card {devices[0]}\n')
        f.write('}\n')

setup_asoundrc()
