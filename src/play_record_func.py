import pyaudio
import wave
import numpy


RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "one.wav"

def audio_datalist_set_volume(chunk, multiply):
    chunk = numpy.fromstring(chunk, numpy.int8) 
    chunk = chunk * multiply
    return chunk.astype(numpy.int8)

def func(WAVE_OUTPUT_FILENAME):
    global RECORD_SECONDS
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
        output_device_index=12,
        frames_per_buffer=CHUNK
    )

    frames = []

    print("* recording")

    # for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    start = 0
    while start < int(RATE / CHUNK * RECORD_SECONDS):
        start += 1
        data = stream.read(CHUNK)  # get audiosteam
        data = audio_datalist_set_volume(data, 2)  # multiply volume
        stream.write(data)  # play audio
        frames.append(data)  # write audio

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

func(WAVE_OUTPUT_FILENAME)
