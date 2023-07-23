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
import signal
import glob

# asound configuration area
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
        text=(f"Sound Sensor theshold exceeded.")
        log_event("raspberrypi",text)
        reset_bounce_count()
        threshold_exceeded("sound",start_hour, start_min, end_hour, end_min)
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
        text=(f"Vibration theshold exceeded. ")
        log_event("raspberrypi",text)
        reset_bounce_count()
        threshold_exceeded("vibration",start_hour, start_min, end_hour, end_min)   
    except Exception as e:
        print(f"Error handling vibration sensor event: {e}")

# Reset bounce counts function
def reset_bounce_count():
    global sound_sensor_bounce_count, vibration_sensor_bounce_count
    counters=f"Reseting Counts: sounds detected: {sound_sensor_bounce_count},vibrations detected: {vibration_sensor_bounce_count}"
    log_event("raspberrypi",counters)
    sound_sensor_bounce_count = 0
    vibration_sensor_bounce_count = 0

# Function to perform specific action when threshold is exceeded
def threshold_exceeded(type,start_hour, start_min, end_hour, end_min):

    current_time = datetime.datetime.now().time() #get current time
    in_target_time_range = is_within_time_range(start_hour,start_min,end_hour,end_min)

    end_time = datetime.time(end_hour, end_min)   #gen end hour
    time_difference = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), current_time) #get difference
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds // 60) % 60

    if type=="sound":
      sayit_text=(f"Be quiet please.")
      sayit(str(sayit_text),volume="-a50",pitch="-p10",word_speed_per_minute="-s150")
    elif in_target_time_range and type=="vibration": 
      if hours > 2 and type=="vibration":
        sayit_text("fHey, It is night time. Close your door. Turn off the lights. Get back in Bed.")
        sayit(str(sayit_text),volume="-a90",pitch="-p10",word_speed_per_minute="-s150")
      elif hours > 0 and type=="vibration":
        sayit_text=(f"Hey, Close your door. There are {hours} hours and {minutes} minutes until morning.")
        sayit(str(sayit_text),volume="-a90",pitch="-p10",word_speed_per_minute="-s150")
      else:
        sayit_text=(f"Hey, Close your door. Only {minutes} minutes until morning.")
        sayit(str(sayit_text),volume="-a90",pitch="-p10",word_speed_per_minute="-s150")
    else:
        sayit_text=f"{type} detected nothing said."

    log_event("raspberrypi",f"threshold_exceeded - {sayit_text}")   

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
#to get this to work I had to convert the audio to a wave and send it using aplay 
def sayit(text,volume,pitch,word_speed_per_minute,debug=1):

  if os.path.exists("/usr/bin/espeak"):
    # Rename the existing output file if it exists
    wav_files = glob.glob("*.wav")

    #remove all the wav files
    for file in wav_files:
      os.remove(file)

    # Call the espeak command and redirect the output to a file
    if debug==1:
      #generate sound clip
      subprocess.call(["espeak", "-w", "output.wav", "-ven-us-nyc+f2","-z","-v",str(volume),str(pitch),str(word_speed_per_minute),text])
      # Convert the mono WAV file to a stereo WAV file
      subprocess.call(["sox", "output.wav", "-c", "2", "-V", "output_stereo.wav","tempo","1.00"])
      #play wave file in headless mode
      subprocess.call(["aplay","-v","-Dplug:default","output_stereo.wav"])
    else: 
      #generate sound clip 
      subprocess.call(["espeak", "-w", "output.wav", "-ven-us-nyc+f2","-z",str(volume),str(pitch),str(word_speed_per_minute),text])
      # Convert the mono WAV file to a stereo WAV file
      subprocess.call(["sox", "output.wav", "-c", "2","output_stereo.wav","tempo","1.00"])
      #play wave file in headless mode
      subprocess.call(["aplay","-Dplug:default","output_stereo.wav"])


    sayit=f"sayit function - espeak: {text}"
    log_event("raspberrypi", sayit) 
  else:
    print("error missing espeak. exiting with 1")
    log_event("raspberrypi", "missing espeak exiting with 1") 
    sys.exit(1)


#############
#MAIN area
#############

# Setup sensor pins
sound_sensor_pin = 4
vibration_sensor_pin = 26

# Initialize sensors
sound_sensor = Button(sound_sensor_pin, bounce_time=0.01)
vibration_sensor = Button(vibration_sensor_pin, bounce_time=0.01)

# Counter variables for each sensor
sound_sensor_bounce_count = 0
vibration_sensor_bounce_count = 0

# Set Threshold values for counters
sound_sensor_threshold = 4
vibration_sensor_threshold = 0

# Define start and end times
start_time = "00:00"
end_time = "6:30"

# Split start and end times into hours and minutes
start_hour, start_min = map(int, start_time.split(":"))
end_hour, end_min = map(int, end_time.split(":"))

#reconfigure the asoundrc file 
#setup_asoundrc()

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
    time.sleep(0.1) #1/10th of second delay 
    current_time = datetime.datetime.now().time()

    # Calculate elapsed time as a timedelta object
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), start_time)
    #print(f"debug elapsed time: {elapsed_time}")

    # Reset bounce counts every reset_interval
    if elapsed_time >= reset_interval:
        reset_bounce_count()
        start_time = current_time
