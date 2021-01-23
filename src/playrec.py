import sounddevice as sd
import soundfile as sf
import numpy as np
import sys

FILE_NAME = 'myfile.flac'
SOUND_FREQUENCY = 48_000
MIN_RECORD_TIME = 5.0
MAX_RECORD_TIME = 10.0 
CHENNELS = 2


array_length = int(MAX_RECORD_TIME) * SOUND_FREQUENCY
storage = np.empty(shape=(array_length, CHENNELS), dtype=np.float32)


recording_is_over = False
current_frame = 0
def callback(indata, outdata, frames, time, status):
    global current_frame, recording_is_over
    if status:
        print(status)

    mod_data = indata * 2
    next_frame = current_frame + frames

    if array_length > next_frame:
        outdata[:] = mod_data
        storage[current_frame:next_frame] = mod_data
        current_frame += frames
    elif not recording_is_over:
        print('#' * 80)
        print('Record is over. Press any kay to close input stream, and save file')
        print('#' * 80)
        recording_is_over = True
    else:
        outdata[:] = mod_data * 0

with sd.Stream(channels=2, callback=callback, samplerate=SOUND_FREQUENCY):
    sd.sleep(1_000)
    print('#' * 80)
    print('input "s" to stop and save record')
    print('#' * 80)
    input_date = input()
    while input_date != "s" or current_frame < int(MIN_RECORD_TIME) * SOUND_FREQUENCY:
        sd.sleep(100)


sf.write('myfile.flac', storage[:current_frame], SOUND_FREQUENCY)

print('#' * 80)
print(f'Record finished, record length: {round(current_frame / SOUND_FREQUENCY, 3)} seconds')
print('#' * 80)
