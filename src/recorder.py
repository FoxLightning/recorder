import argparse
import sys
from threading import Thread

import numpy as np
import sounddevice as sd
import soundfile as sf

from tests.test_input_device import init_input_test
from tests.test_output_device import init_output_test
from utils import json_manipulator
from utils.generate_path import default_path

# configuration variables
FILE_NAME = 'my_record.flac'
SOUND_FREQUENCY = 48_000
MIN_RECORD_TIME = 5.0
MAX_RECORD_TIME = 60.0
CHENNELS = 2

# technical variables
array_length = int(MAX_RECORD_TIME) * SOUND_FREQUENCY
min_frame = int(MIN_RECORD_TIME) * SOUND_FREQUENCY

# global variables
storage = np.empty(shape=(array_length, CHENNELS), dtype=np.float32)
run_record = True
current_frame = 0
input_alive = True

# init json manipulator
device_io = json_manipulator.DevicesIO()


def callback(indata, outdata, frames, time, status):
    global run_record, current_frame, storage
    if status:
        print(status)

    mod_data = indata * 2  # change input sound
    next_frame = current_frame + frames

    if next_frame < array_length:
        outdata[:] = mod_data  # redirect sound
        storage[current_frame:next_frame] = mod_data  # write sounddata to RAM
        current_frame += frames
    else:
        run_record = False


def record(callback, samplerate, record_time):
    global run_record
    with sd.Stream(channels=2, callback=callback, samplerate=samplerate):
        while run_record or current_frame < min_frame:
            sd.sleep(100)


def record_control():
    global run_record, input_alive
    sd.sleep(500)  # write print below after warning log
    print('Input "s" to stop record')

    while input_alive and run_record:
        input_data = input()
        if input_data == 's':
            run_record = False
            input_alive = False
            break
        elif input_alive and run_record:
            print('Incorect input. Input "s" to stop record')


def apply_and_show_devices():
    sd.default.device = int(device_io.get_input()), int(device_io.get_output())
    print('#' * 80)
    print('Device list')
    device_list = sd.query_devices(device=None, kind=None)
    print(device_list)


def fast_device_choice():
    apply_and_show_devices()
    id_input_device = input('Enter id of input device: ')
    id_output_device = input('Enter id of output device: ')
    device_io.set_input(id_input_device)
    device_io.set_output(id_output_device)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    return parser


if __name__ == "__main__":
    # prase args, create path
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    path = namespace.path if namespace.path else default_path()

    # choice the i/o device
    input_data = ''
    while input_data != 'r':
        print("Press 't' test and choice i/o device")
        print("Press 'f' fast choice i/o device")
        print("Press 's' show choisen i/o device")
        print("Press 'r' start record")
        input_data = input().lower()
        if input_data == 't':
            init_output_test()
            init_input_test()
            device_io = json_manipulator.DevicesIO()
            apply_and_show_devices()
        elif input_data == 'f':
            fast_device_choice()
            apply_and_show_devices()
        elif input_data == 's':
            apply_and_show_devices()

    # create threes
    record_tree = Thread(target=record,
                         args=(callback, SOUND_FREQUENCY, MAX_RECORD_TIME))
    input_tree = Thread(target=record_control)

    # start threes
    record_tree.start()
    sd.sleep(400)  # write print below after warning log
    print('* record')
    input_tree.start()

    # join write three and save data
    record_tree.join()
    # write sound data to persistent storage
    sf.write(path, storage[:current_frame], SOUND_FREQUENCY)
    length = current_frame / SOUND_FREQUENCY
    print(f'Record finished, length: {round(length, 3)}')

    # close input
    if input_alive:
        print('Input something to exit')
    input_tree.join()
