



import pyaudio
import numpy as np
import time

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

rms=get_sound_level()
# Print the sound level
if rms < 100:
 print(f"Low Sound level: {rms:.2f}")
elif rms >= 150 and rms < 250:
 print(f"Moderate Sound level: {rms:.2f}")
else:
 print(f"Moderate Sound level: {rms:.2f}")

