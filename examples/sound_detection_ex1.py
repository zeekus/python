#!/usr/bin/python3
#filename: sound_detection_ex1.py
#description: read data from the sound sensor module and calculate the noise level

#modules -  python-pyaudio python3-pyaudio

import pyaudio
import math

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while True:
    data = stream.read(CHUNK)
    rms = math.sqrt(sum([x*x for x in data])/len(data))
    db = 20 * math.log10(rms)
    if db > THRESHOLD:
        print("Noise level: {:.2f} dB".format(db))

stream.stop_stream()
stream.close()
p.terminate()