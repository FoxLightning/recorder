import sounddevice as sd
import soundfile as sf
import numpy as np
import sys


SOUND_FREQUENCY = 48_000
MIN_RECORD_TIME = 5.0
MAX_RECORD_TIME = 10.0  # seconds, only float
CHENNELS = 2


array_length = int(MAX_RECORD_TIME) * SOUND_FREQUENCY
storage = np.empty(shape=(array_length, CHENNELS), dtype=np.float32)


current_frame = 0
def callback(indata, outdata, frames, time, status):
    global current_frame
    if status:
        print(status)

    mod_data = indata * 2
    next_frame = current_frame + frames

    if array_length > next_frame:
        outdata[:] = mod_data
        storage[current_frame:next_frame] = mod_data
        current_frame += frames
    else:
        print('Stop')
        return

stream = sd.Stream(channels=2, samplerate=SOUND_FREQUENCY)
stream.start()

while True:
    callback()

stream.stop()



