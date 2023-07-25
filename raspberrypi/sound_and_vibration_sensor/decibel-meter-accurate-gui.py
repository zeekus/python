import tkinter as tk
import numpy as np
import pyaudio
import tk_tools
from numpy.polynomial import Polynomial
from scipy.signal import bilinear, lfilter
#source: https://codereview.stackexchange.com/questions/279980/python-decibel-meter-accurate


CHUNKS = [4096, 9600]
CHUNK = CHUNKS[1]
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATES = [44100, 48000]
RATE = RATES[1]


def A_weighting(fs: float) -> tuple[np.ndarray, np.ndarray]:
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    a1000 = 1.9997

    nums = Polynomial(((2*np.pi * f4)**2 * 10**(a1000 / 20), 0,0,0,0))
    dens = (
        Polynomial((1, 4*np.pi * f4, (2*np.pi * f4)**2)) *
        Polynomial((1, 4*np.pi * f1, (2*np.pi * f1)**2)) *
        Polynomial((1, 2*np.pi * f3)) *
        Polynomial((1, 2*np.pi * f2))
    )
    return bilinear(nums.coef, dens.coef, fs)


def rms_flat(a: np.ndarray) -> float:
    return np.sqrt(a.dot(a) / len(a))


class Meter:
    def __init__(self) -> None:
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=FORMAT,
            channels=CHANNEL,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        self.numerator, self.denominator = A_weighting(RATE)
        self.max_decibel = 0

    def __enter__(self) -> 'Meter':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def listen(self, offset: int) -> float:
        block = self.stream.read(CHUNK)
        decoded_block = np.frombuffer(block, dtype=np.int16)
        y = lfilter(self.numerator, self.denominator, decoded_block)
        new_decibel = 20*np.log10(rms_flat(y)) + offset
        self.max_decibel = max(self.max_decibel, new_decibel)
        return new_decibel


class GUI:
    def __init__(self, meter: Meter) -> None:
        self.meter = meter

        self.root = root = tk.Tk()
        root.title('Decibel Meter')
        root.grid()
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.app_closed = False

        self.gaugedb = tk_tools.RotaryScale(root, max_value=120, unit=' dBA')
        self.gaugedb.grid(column=1, row=1)

        self.led = tk_tools.Led(root, size=50)
        self.led.grid(column=3, row=1)
        self.led.to_red(on=False)

        tk.Label(root, text='Too Loud').grid(column=3, row=0)
        tk.Label(root, text='Max').grid(column=2, row=0)
        tk.Label(root, text='Calibration (dB)').grid(column=4, row=0)

        self.maxdb_display = tk_tools.SevenSegmentDigits(root, digits=3, digit_color='#00ff00', background='black')
        self.maxdb_display.grid(column=2, row=1)

        self.offset = tk.IntVar(root, value=0, name='offset')
        spinbox = tk.Spinbox(root, from_=-20, to=20, textvariable=self.offset, state='readonly')
        spinbox.grid(column=4, row=1)

    def close(self) -> None:
        self.app_closed = True

    def run(self) -> None:
        while not self.app_closed:
            new_decibel = self.meter.listen(self.offset.get())
            self.update(new_decibel, self.meter.max_decibel)
            self.root.update()

    def update(self, new_decibel: float, max_decibel: float) -> None:
        self.gaugedb.set_value(np.around(new_decibel, 1))
        self.maxdb_display.set_value(f'{max_decibel:.1f}')
        self.led.to_red(on=new_decibel > 85)


def main() -> None:
    with Meter() as meter:
        gui = GUI(meter)
        gui.run()
