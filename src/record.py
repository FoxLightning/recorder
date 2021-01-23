import sounddevice as sd
import numpy as np
from time import sleep


duration = 10  # seconds
fs = 48000
# array
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sleep(duration)

sd.play(myrecording, fs)
breakpoint()
sleep(duration)

sd.stop()

