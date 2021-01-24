# recorder

## Manual
1. To run from {our path}/recorder/
    a) files will be saved in {our path}/recorder/src/records/
       name consist from date and time
    $ python3 src/recorder.py
    b) files will be saved in {input}
    $ python3 src/recorder.py -p {input} 
2. You choice and test device for input and output sound
    a) 't' test and choice i/o device
            at first, script goes throught all output devices and gives them a sound
        if you hire the sound and wont to choise device, type y
            at last, script goes throught all input devices and redirect sound from
        their to choisen output device
    b) 'f' print list of avilable devices and id of devices what you want to choice
    c) 's' show avilable devices
3. 'r' to run record
4. Minimym record time: 5 seconds, maximum record time: 60 second
5. enter 's' when record start - to stop record if you enter faster then 5 seconds 
    after start, record will stoped at 5 second after start

