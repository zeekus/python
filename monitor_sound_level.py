import pyaudio
import numpy as np

# Set the parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (Hz)
CHUNK = 1024  # Buffer size

# Create an instance of the PyAudio class
audio = pyaudio.PyAudio()

# Open a stream to capture audio from the USB microphone
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Loop over the audio stream and calculate the sound levels
while True:
    # Read audio data from the stream
    data = stream.read(CHUNK)

    # Convert the audio data to a numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Calculate the root mean square (RMS) of the audio data
    rms = np.sqrt(np.mean(np.square(audio_data)))

    # Print the sound level
    print(f"Sound level: {rms:.2f}")

# Close the audio stream and PyAudio instance when done
stream.stop_stream()
stream.close()
audio.terminate()
