import sounddevice as sd

from audio2numpy import open_audio

from time import sleep



import numpy as np
from numpy import linspace, sin, pi, int16 
import sounddevice as sd

sampling_rate = 44_100
length_seconds = 5

def sound_func(argument, sound_frequency=500, sampling_rate=48_000, sound_tone=500, amplitude=1):
    step = argument / sampling_rate
    func_value = amplitude * sin(sound_frequency * 2 * pi * step)
    return func_value

def generate_sound(sampling_rate, length_seconds):
    array_length = int(length_seconds) * sampling_rate
    semple = np.empty(shape=(array_length, 2), dtype=np.float32)
    for n in range(array_length):
        semple[n] += sound_func(n)
    return semple




signal = generate_sound(sampling_rate, length_seconds)

sd.play(signal, sampling_rate)

print(sampling_rate)
sleep(5)

sd.stop()
