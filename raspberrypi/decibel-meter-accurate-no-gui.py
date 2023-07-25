import numpy as np
import pyaudio
from numpy.polynomial import Polynomial
from scipy.signal import bilinear, lfilter
import time
import datetime


# Define the chunk size for the audio stream
CHUNKS = [4096, 9600]
CHUNK = CHUNKS[1]

# Define the audio format, number of channels, and sampling rate
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATES = [44100, 48000]
RATE = RATES[1]

# Define the A-weighting filter coefficients
def A_weighting(fs: float) -> tuple[np.ndarray, np.ndarray]:
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    a1000 = 1.9997

    # Define the numerator and denominator polynomials for the A-weighting filter
    nums = Polynomial(((2*np.pi * f4)**2 * 10**(a1000 / 20), 0,0,0,0))
    dens = (
        Polynomial((1, 4*np.pi * f4, (2*np.pi * f4)**2)) *
        Polynomial((1, 4*np.pi * f1, (2*np.pi * f1)**2)) *
        Polynomial((1, 2*np.pi * f3)) *
        Polynomial((1, 2*np.pi * f2))
    )
    # Apply bilinear transformation to convert the analog filter to a digital filter
    return bilinear(nums.coef, dens.coef, fs)

# Define the root-mean-square (RMS) function for a flat signal
def rms_flat(a: np.ndarray) -> float:
    return np.sqrt(a.dot(a) / len(a))

# Define the Meter class for measuring decibel levels
class Meter:
    def __init__(self) -> None:
        # Initialize the PyAudio object and open the audio stream
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=FORMAT,
            channels=CHANNEL,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        # Calculate the A-weighting filter coefficients for the sampling rate
        self.numerator, self.denominator = A_weighting(RATE)
        # Initialize the maximum decibel level to 0
        self.max_decibel = 0

    def __enter__(self) -> 'Meter':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Stop and close the audio stream and terminate the PyAudio object
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def listen(self, offset: int) -> float:
        # Read a chunk of audio data from the stream
        block = self.stream.read(CHUNK)
        # Convert the audio data to a NumPy array of 16-bit integers
        decoded_block = np.frombuffer(block, dtype=np.int16)
        # Apply the A-weighting filter to the audio data
        y = lfilter(self.numerator, self.denominator, decoded_block)
        # Calculate the decibel level of the filtered audio data with the given offset
        new_decibel = 20*np.log10(rms_flat(y)) + offset
        # Update the maximum decibel level
        self.max_decibel = max(self.max_decibel, new_decibel)
        # Return the new decibel level
        return new_decibel

# Define the main function for logging decibel levels
def main(formatted_time) -> None:
    # Create a Meter object for measuring decibel levels
    with Meter() as meter:
        # Open a file for writing the decibel levels
        with open('decibel_log.txt', 'a') as f:
            # Get the start time of the loop
            start_time = time.time()
            # Loop for 1 second
            while time.time() - start_time < 1:
                # Measure the decibel level with an offset of 0
                new_decibel = meter.listen(0)
                # Write the decibel level to the file
                formatted_time = current_time.strftime('%H:%M:%S.%f')[:-3]
                f.write(f'{formatted_time} {new_decibel:.1f}\n')
                # Wait for 0.1 seconds before measuring the next decibel level
                time.sleep(0.1)
                return new_decibel


while True:
    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime('%H:%M:%S.%f')[:-3]
    decibel=main(formatted_time)
    print(f'{formatted_time} {decibel:.1f}')
    
