from time import sleep, time
from threading import Thread
import sys

MIN_TIME = 5
MAX_TIME = 10

def foo():
    print('Start')
    global seconds
    start = 0
    while start < seconds:
        start += 1
        sleep(1)
    print('Finish')

start = time() # starting time

seconds = MAX_TIME 
th1 = Thread(target=foo)
th1.start()  # start three MAX_TIME

print("type 's' for stop recording\nCtrl+D to out from input mode")
a = sys.stdin.readline().strip()
seconds = MIN_TIME if a == 's' else MAX_TIME

th1.join()

print(f'Time: {time() - start}')