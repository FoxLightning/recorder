import sys
import wave
from threading import Thread

import numpy
import pyaudio

import mute_alsa  # noqa

MIN_RECORD_SECONDS = 5
MAX_RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "one.wav"


def audio_datalist_set_volume(chunk, multiply):
    chunk = numpy.fromstring(chunk, numpy.int8)
    chunk = chunk * multiply
    return chunk.astype(numpy.int8)


def record(WAVE_OUTPUT_FILENAME):
    global MAX_RECORD_SECONDS
    CHUNK = 64
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        input_device_index=7,
        output_device_index=11,
        frames_per_buffer=CHUNK
    )

    frames = []

    print("* recording")

    start = 0
    while start < int(RATE / CHUNK * MAX_RECORD_SECONDS):
        start += 1
        data = stream.read(CHUNK)  # get audiosteam
        data = audio_datalist_set_volume(data, 2)  # multiply volume
        stream.write(data)  # play audio
        frames.append(data)  # write audio
    print(start * CHUNK / RATE)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == "__main__":
    WAVE_OUTPUT_FILENAME = sys.argv[1]

    th1 = Thread(target=record, args=(WAVE_OUTPUT_FILENAME,))
    th1.daemon = True
    th1.start()  # start three MAX_TIME

    print("type 's' for stop recording\nCtrl+D to out from input mode")
    a = sys.stdin.readline().strip()

    MAX_RECORD_SECONDS = MIN_RECORD_SECONDS if a == 's' else MAX_RECORD_SECONDS

    th1.join()