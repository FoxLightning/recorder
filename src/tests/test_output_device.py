import numpy as np
from numpy import linspace, sin, pi, int16 
import sounddevice as sd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from utils import json_manipulator


def sound_func(sampling_step, sound_frequency=500, sampling_rate=48_000, max_amplitude=1):
    """
    Generates sound amplitude at a specific time
    """
    time_step = sampling_step / sampling_rate
    
    # sound function 
    func_value = max_amplitude * sin(sound_frequency * 2 * pi * time_step)
    return func_value


def generate_sound(sampling_rate, length_seconds):
    """
    Generates a numpy array of sound amplitude at a specific time
    """
    # create empty numpy array with given length
    array_length = int(length_seconds) * sampling_rate  
    semple = np.empty(shape=(array_length, 2), dtype=np.float32)  

    # fill array
    for n in range(array_length): 
        semple[n] += sound_func(n)
    return semple


def play_audio(signal, samplerate, seconds=5):
    sd.play(signal, samplerate)
    sd.sleep(int(seconds) * 1_000)
    sd.stop()


def init_output_test():
    sampling_rate = 48_000
    length_seconds = 5

    # initializate json manipulator
    device_io = json_manipulator.DevicesIO()

    # generate sound sample
    sound_sample = generate_sound(sampling_rate, length_seconds)

    # get device list
    device_list = sd.query_devices(device=None, kind=None)

    # go through all output devices
    for id, device in enumerate(device_list):
        if device['max_output_channels']:
            print(id, device['name'])
            sd.default.device = id
            play_audio(signal=sound_sample, samplerate=sampling_rate)
            
            print("'y' set this device as active and exit")
            print("any key - go to test next device")
            input_value = input()
            if input_value.lower() == 'y':
                device_io.set_output(id)
                break


if __name__ == "__main__":
    init_output_test()
