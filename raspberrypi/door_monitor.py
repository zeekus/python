#filename: door_monitor.py
#description: The program monitors the door and preforms actions when certain conditions are me.t
#The goal of this is to tell my kid to go to sleep when he wakes during the target hours which are 22:00 (10:30PM) to 06:30 (6:30AM)

import RPi.GPIO as GPIO
import datetime 
import time
import os 
import subprocess
import sys
import glob
import pyaudio
import numpy

# handlers area
def is_door_open():
    if GPIO.input(21):
        return True
    else:
        return False

def get_sound_level():
  # Set the parameters for audio recording
  FORMAT = pyaudio.paInt16
  CHANNELS = 1  # Mono audio
  #RATE = 44100  # Sample rate (Hz)
  RATE = 96000  # Sample rate (Hz)
  CHUNK = 1024  # Buffer size
  # Create an instance of the PyAudio class
  audio = pyaudio.PyAudio()
  # Open a stream to capture audio from the USB microphone
  stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

  # Read audio data from the stream
  data = stream.read(CHUNK)

  # Convert the audio data to a numpy array
  audio_data = np.frombuffer(data, dtype=np.int16)
 
  # Calculate the root mean square (RMS) of the audio data
  try: 
    rms = np.sqrt(np.mean(np.square(audio_data)))
  except: 
    print("we got an error")

  # Close the audio stream and PyAudio instance when done
  stream.stop_stream()
  stream.close()
  audio.terminate()
  # Return the current sound level 
  return rms


# Function to perform specific action when threshold is exceeded
def action_triggered(type,start_hour, start_min, end_hour, end_min):

    current_time = datetime.datetime.now().time() #get current time
    in_target_time_range = is_within_time_range(start_hour,start_min,end_hour,end_min)

    end_time = datetime.time(end_hour, end_min)   #gen end hour
    time_difference = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), current_time) #get difference
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds // 60) % 60


    if in_target_time_range and type=="door": 
      if hours > 2 and type=="door":
        sayit_text=(f"Close your door. Turn off the lights. Get back in Bed. It is night time.")
        sayit(str(sayit_text),volume="90")
      elif hours > 0 and type=="door":
        sayit_text=(f"Hey, Close your door. There are {hours} hours and {minutes} minutes until morning.")
        ayit(str(sayit_text),volume="90")
      else:
        sayit_text=(f"Hey, Close your door. Only {minutes} minutes until morning.")
        sayit(str(sayit_text),volume="90")
    else:
        sayit_text=f"{type} detected - nothing said."

    log_event("raspberrypi",f"{type} action_triggered - {sayit_text} in_target_time_range {in_target_time_range}")   

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

    #text=f"debug: is_within_time_range: current_datetime_est {current_datetime_est}"
    #log_event("raspberrypi", text) 

    start_datetime,end_datetime=adjust_time_for_days(current_datetime_est,start_hour,start_min,end_hour,end_min)
 
    if start_datetime <= current_datetime <= end_datetime:
        my_return=True
    else:
        my_return=False

    #text=f"debug: is_within_time_range: value returned {my_return}"
    #log_event("raspberrypi", text) 
   
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
def sayit(text,volume):

  if os.path.exists("/usr/bin/espeak"):
    # Rename the existing output file if it exists
    wav_files = glob.glob("*.wav")

    #remove all the wav files
    for file in wav_files:
      os.remove(file)

    # Call the espeak command and redirect the output to a file
    #espeak ref: -a 100 max volume
    subprocess.call(["espeak", "-w", "output.wav", "-ven-us-nyc+f2","-z","-a",volume,"-p 10","-s150", text])

    # Convert the mono WAV file to a stereo WAV file
    subprocess.call(["sox", "output.wav", "-c", "2", "output_stereo.wav"])
    #subprocess.call(["sox", "output.wav", "-c", "2", "-V", "output_stereo.wav"])
    
    #play the audio file using aplay
    subprocess.call(["aplay","-Dplug:default","output_stereo.wav"])
    sayit=f"sayit - espeak: {text}"
    log_event("raspberrypi", sayit) 
  else:
    print("error missing espeak. exiting with 1")
    log_event("raspberrypi", "missing espeak exiting with 1") 
    sys.exit(1)

#############
#MAIN area
#############

# Setup door sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Define start and end times
start_time = "00:00"
end_time = "06:30"

# Split start and end times into hours and minutes
start_hour, start_min = map(int, start_time.split(":"))
end_hour, end_min = map(int, end_time.split(":"))


# Time Tracking
start_time = datetime.datetime.now().time()

log_event("raspberrypi", f"*** starting monitoring script ***" )

# Keep the program running
while True:
    time.sleep(.5) #delay .5 second
    current_time = datetime.datetime.now().time()

    # Calculate elapsed time as a timedelta object
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), start_time)

    if is_door_open() == True:
        action_triggered("door",start_hour, start_min, end_hour, end_min)
