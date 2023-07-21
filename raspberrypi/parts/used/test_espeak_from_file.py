import os
import subprocess
import glob

# Set the text to be spoken
text = "testing 1 2 3"

# Rename the existing output file if it exists
wav_files = glob.glob("*.wav")

#remove all the wav files
for file in wav_files:
    os.remove(file)

# Call the espeak command and redirect the output to a file
subprocess.call(["espeak", "-w", "output.wav", "-ven-us", "-s150", "-z","-a","500","-p 1", text])

# Convert the mono WAV file to a stereo WAV file
subprocess.call(["sox", "output.wav", "-c", "2", "output_stereo.wav","tempo","0.9"])

subprocess.call(["aplay","-Dplug:default","output_stereo.wav"])

