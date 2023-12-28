#!/usr/bin/python3
import time
import os
import subprocess
import sys
import glob

def sayit( text, volume):
        if os.path.exists("/usr/bin/espeak"):
            wav_files = glob.glob("*.wav")

            for file in wav_files:
                os.remove(file)
            subprocess.call(["espeak", "-w", "output.wav", "-ven-gb+m1", "-z", "-a", volume, "-p", "1", "-s150", "-g", "5", "-k", "5", "-m", text])
            subprocess.call(["sox", "output.wav", "-c", "2", "output_stereo.wav"])
            subprocess.call(["aplay", "-Dplug:default", "output_stereo.wav"])

            sayit = f"sayit - espeak: {text}"
        else:
            print("error missing espeak. exiting with 1")
            sys.exit(1)

        time.sleep(5) #only talk every 15 seconds. 


pid = os.fork()
if pid == 0:
  sayit_text = f"test"
  sayit(str(sayit_text), volume="200")
else:
  time.sleep(0)

print("done - without waiting")


