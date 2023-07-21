import subprocess
import glob
import os

# Generate a WAV file with Festival
text = "Testing 1 2 3 "
wav_file = "output.wav"

# Rename the existing output file if it exists
wav_files = glob.glob("*.wav")

#remove all the wav files
for file in wav_files:
    os.remove(file)

# Call the espeak command and redirect the output to a file
subprocess.run(["text2wave", "-o", wav_file], input=text.encode(), check=True)

# Convert the mono WAV file to a stereo WAV file
subprocess.call(["sox", "output.wav", "-c", "2", "output_stereo.wav","tempo","0.9"])

subprocess.call(["aplay","-Dplug:default","output_stereo.wav"])

