import os
import subprocess

# Set the text to be spoken
text = "Hello, world!"

# Rename the existing output file if it exists
if os.path.exists("output.wav"):
    os.rename("output.wav", "output_old.wav")

# Call the espeak command and redirect the output to a file
subprocess.call(["espeak", "-w", "output.wav", "-ven-us", "-s150", "-z", text])

# Convert the mono WAV file to a stereo WAV file
subprocess.call(["sox", "output.wav", "-c", "2", "output_stereo.wav","tempo","0.8"])

#sounds like a chipmunk but works
subprocess.call(["aplay", "output_stereo.wav"])
