# recorder

## Manual
1. To run from {our path}/recorder/ <br>
    a) files will be saved in {our path}/recorder/src/records/ <br>
       name consist from date and time <br>
    $ python3 src/recorder.py <br>
    b) files will be saved in {input} <br>
    $ python3 src/recorder.py -p {input}  <br>
2. You choice and test device for input and output sound <br>
    a) 't' test and choice i/o device <br>
            at first, script goes throught all output devices and gives them a sound <br>
        if you hire the sound and wont to choise device, type y <br>
            at last, script goes throught all input devices and redirect sound from <br>
        their to choisen output device <br>
    b) 'f' print list of avilable devices and id of devices what you want to choice <br>
    c) 's' show avilable devices <br>
3. 'r' to run record <br>
4. Minimym record time: 5 seconds, maximum record time: 60 second <br>
5. enter 's' when record start - to stop record if you enter faster then 5 seconds  after start, record will stoped at 5 second after start
