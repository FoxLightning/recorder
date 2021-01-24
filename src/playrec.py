import sys
from threading import Thread

import numpy as np
import sounddevice as sd
import soundfile as sf


# configuration variables
FILE_NAME = 'my_record.flac'
SOUND_FREQUENCY = 48_000
MIN_RECORD_TIME = 5.0
MAX_RECORD_TIME = 10.0 
CHENNELS = 2

# technical variables
array_length = int(MAX_RECORD_TIME) * SOUND_FREQUENCY
min_frame = int(MIN_RECORD_TIME) * SOUND_FREQUENCY

# global variables
storage = np.empty(shape=(array_length, CHENNELS), dtype=np.float32)
run_record = True
current_frame = 0
input_alive = True


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
    print(f'Input "s" to stop record')

    while input_alive and run_record:
        input_data = input()
        if input_data == 's':
            run_record = False
            input_alive = False
            break
        elif input_alive and run_record:
            print('Incorect input. Input "s" to stop record')


if __name__ == "__main__":
    # # choice the i/o device
    # device_list = sd.query_devices(device=None, kind=None)
    # print(device_list)
    # input('Enter id of input devie: ')
    # input('Enter id of output devie: ')

    # create threes
    record_tree = Thread(target=record, args=(callback, SOUND_FREQUENCY, MAX_RECORD_TIME))
    input_tree = Thread(target=record_control)

    # start threes
    record_tree.start()
    sd.sleep(400)  # write print below after warning log
    print(f'* record')
    input_tree.start()

    # join write three and save data
    record_tree.join()
    sf.write('myfile.flac', storage[:current_frame], SOUND_FREQUENCY)  # write sound data to persistent storage
    print(f'Record finished, length: {round(current_frame / SOUND_FREQUENCY, 3)}')  # info
    
    # close input
    if input_alive:
        print(f'Input something to exit')
    input_tree.join()
