import sys
from threading import Thread

import numpy as np
import sounddevice as sd
import soundfile as sf

from sounddevice import PortAudioError

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from utils import json_manipulator


def callback(indata, outdata, frames, time, status):
    """
    redirect sound from input device to output device
    """
    if status:
        print(status)
    outdata[:] = indata




def init_input_test():
# if __name__ == "__main__":
    SAMPLING_RATE = 48_000
    TEST_LENGTH = 5

    # initializate json manipulator
    device_io = json_manipulator.DevicesIO()

    # get device list
    device_list = sd.query_devices(device=None, kind=None)

    # go through all input devices
    for id, device in enumerate(device_list):
        try:
            if device['max_input_channels']:
                print(id, device['name'])
                sd.default.device = id, device_io.get_output()
                exit_condition = False

                with sd.Stream(channels=1, callback=callback, samplerate=SAMPLING_RATE):
                    sd.sleep(TEST_LENGTH * 1_000)

                print("'y' set this device as active and exit")
                print("any key - go to test next device")
                input_value = input()
                if input_value.lower() == 'y':
                    device_io.set_input(id)
                    exit_condition = True
                    break
        except PortAudioError:
            print('something goes wrong with previous device')


if __name__ == "__main__":
    init_input_test()
