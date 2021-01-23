import sounddevice as sd

from audio2numpy import open_audio

from time import sleep


fp = "/home/fox/Documents/git_repositories/recorder/src/star.mp3"
signal, sampling_rate = open_audio(fp)

sd.play(signal, sampling_rate)

print(sampling_rate)
sleep(500)

sd.stop()