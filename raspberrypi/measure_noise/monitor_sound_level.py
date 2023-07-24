import pyaudio
import numpy as np
import time
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
max_val= float('-inf')
min_val= float('inf')
count =0
# Loop over the audio stream and calculate the sound levels
while True and count < 100:
    # Read audio data from the stream
    data = stream.read(CHUNK)

    # Convert the audio data to a numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Calculate the root mean square (RMS) of the audio data
    try: 
      rms = np.sqrt(np.mean(np.square(audio_data)))
    except: 
      rms=0

    if rms>max_val:
        max_val=rms
    if rms<min_val:
        min_val=rms

    # Print the sound level
    if rms > 50:
      print(f"{count} Sound level: {rms:.2f}")
    count = count+1


    time.sleep(.1)

# Close the audio stream and PyAudio instance when done
stream.stop_stream()
stream.close()
audio.terminate()
print(f"max value: {max_val}")
print(f"min value: {min_val}")
