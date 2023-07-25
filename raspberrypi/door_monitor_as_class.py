import RPi.GPIO as GPIO
import datetime
import time
import os
import subprocess
import sys
import glob
import pyaudio
import numpy as np

def start_timer():
    return time.time()

class DoorMonitor:
    def __init__(self):
        # Setup door sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.timer_start = None

    def is_door_open(self):
        if GPIO.input(21):
            if self.timer_start is None:
                # Start the timer when the door is opened
                self.timer_start = time.time()
            return True
        else:
            if self.timer_start is not None:
                # Stop the timer when the door is closed
                elapsed_time = time.time() - self.timer_start
                self.timer_start = None
                self.log_event("raspberrypi", f"Door was open for {elapsed_time:.2f} seconds")
            return False

    def get_sound_level(self):
        # Set the parameters for audio recording
        pass 

    def action_triggered(self, type, start_hour, start_min, end_hour, end_min,debug=0):
        # Start the timer
        start_time = start_timer()

        current_time = datetime.datetime.now().time()
        in_target_time_range = self.is_within_time_range(start_hour, start_min, end_hour, end_min)

        end_time = datetime.time(end_hour, end_min)
        time_difference = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(
            datetime.date.today(), current_time)
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds // 60) % 60

        if in_target_time_range and type == "door":
            if hours > 2 and type == "door":
                sayit_text = "Hey, Close your door. It is night time. Turn off the lights. Get back in Bed."
                self.sayit(str(sayit_text), volume="90")
            elif hours > 0 and type == "door":
                sayit_text = f"Hey, Close your door. Morning is in {hours} hours and {minutes} minutes."
                self.sayit(str(sayit_text), volume="90")
            else:
                sayit_text = f"Hey, Close your door. You have {minutes} minutes until {end_hour:02d}:{end_min:02d}."
                self.sayit(str(sayit_text), volume="90")
        else:
            sayit_text = f"{type} open - nothing said."

        # Stop the timer and log the elapsed time
        elapsed_time = time.time() - start_time

        if debug ==1:
          self.log_event("raspberrypi", f"{type} action_triggered - {sayit_text} in_target_time_range {in_target_time_range}")

    def adjust_time_for_days(self, current_datetime, start_hour, start_min, end_hour, end_min):
        start_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(start_hour, start_min, 0))
        end_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(end_hour, end_min, 0))

        if end_datetime < start_datetime:
            end_datetime += datetime.timedelta(days=1)

        return start_datetime, end_datetime

    def is_within_time_range(self, start_hour, start_min, end_hour, end_min):
        current_datetime = datetime.datetime.now()
        env_tz = os.environ.get('TZ')

        if env_tz and 'EST' in env_tz:
            est_offset = datetime.timedelta(hours=5)
        else:
            est_offset = datetime.timedelta(hours=0)

        current_datetime_est = current_datetime - est_offset

        start_datetime, end_datetime = self.adjust_time_for_days(current_datetime_est, start_hour, start_min,
                                                                 end_hour, end_min)

        if start_datetime <= current_datetime <= end_datetime:
            return True
        else:
            return False

    def log_event(self, filestring, text):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_name = f"{filestring}_{current_date}.log"
        log_message = f"{datetime.datetime.now()} - {text}\n"
        print(log_message.rstrip("\n"))

        with open(log_file_name, "a") as log_file:
            log_file.write(log_message)

    def sayit(self, text, volume):
        if os.path.exists("/usr/bin/espeak"):
            wav_files = glob.glob("*.wav")

            for file in wav_files:
                os.remove(file)

            subprocess.call(["espeak", "-w", "output.wav", "-ven-us-nyc+f2", "-z", "-a", volume, "-p 10", "-s150", text])
            subprocess.call(["sox", "output.wav", "-c", "2", "output_stereo.wav"])
            subprocess.call(["aplay", "-Dplug:default", "output_stereo.wav"])

            sayit = f"sayit - espeak: {text}"
            self.log_event("raspberrypi", sayit)
        else:
            print("error missing espeak. exiting with 1")
            self.log_event("raspberrypi", "missing espeak exiting with 1")
            sys.exit(1)

        time.sleep(15) #only talk every 15 seconds. 

# Create an instance of the DoorMonitor class
door_monitor = DoorMonitor()

# Define start and end times
start_time = "00:00"
end_time = "06:30"

# Split start and end times into hours and minutes
start_hour, start_min = map(int, start_time.split(":"))
end_hour, end_min = map(int, end_time.split(":"))

# Time Tracking
start_time = datetime.datetime.now().time()

door_monitor.log_event("raspberrypi", f"*** starting monitoring script ***")

# Keep the program running
while True:
    time.sleep(.1)
    current_time = datetime.datetime.now().time()

    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(
        datetime.date.today(), start_time)

    if door_monitor.is_door_open():
        door_monitor.action_triggered("door", start_hour, start_min, end_hour, end_min)
