from wavebender import sine_wave, compute_samples, write_wavefile
from itertools import chain, islice

from src import generate_packet

import time
from datetime import datetime
import calendar

HIGH_BIT_FREQ = 2500. #Logical level 1
LOW_BIT_FREQ = 2000.  #Logical level 0

BEEP_FREQ = 1000. #Acoustic reference beep

def get_frame(bits):
    wave = None
    for bit in bits:
        data = generate_wave(LOW_BIT_FREQ) if bit == '0' else generate_wave(HIGH_BIT_FREQ)
        wave = data if wave is None else chain(wave, data)
    return wave


def beep_wave1():
    return chain(
        generate_wave(BEEP_FREQ, duration=0.1, amplitude=1),
        generate_wave(BEEP_FREQ, amplitude=0.00000001, duration=0.9)
    )

def beep_wave2():
    return chain(
        generate_wave(BEEP_FREQ, duration=0.1, amplitude=1),
        generate_wave(BEEP_FREQ, amplitude=0.00000001, duration=1.9)

    )


def silent_wave():
    return generate_wave(BEEP_FREQ, amplitude=0.000001, duration=1)


def generate_wave(frequency=BEEP_FREQ, framerate=44100, amplitude=1, duration=0.03):
    return islice(sine_wave(frequency, framerate, amplitude), duration*framerate)


def segment_one(bits):
    return chain(
        get_frame(bits),
        generate_wave(BEEP_FREQ, amplitude=0.000001, duration=0.04)
    )


def segment_two(bits):
    return chain(get_frame(bits), generate_wave(BEEP_FREQ, amplitude=0.000001, duration=0.52))


def audio_src(date):
    p1, p2, warning =  generate_packet(date)

    year=date.year
    day_number_in_month=date.day
    hours=date.hour
    minutes=date.minute
    month=date.month

    global p3
    p3=0

    if(warning != "00"):
        if((warning == "10" and month == 1 and day_number_in_month == 1 and hours == 0 and minutes == 59) or (warning == "10" and month == 7 and day_number_in_month == 1 and hours == 1 and minutes == 59)):
            p3=2
        elif((warning == "11" and month == 1 and day_number_in_month == 1 and hours == 0 and minutes == 59) or (warning == "11" and month == 7 and day_number_in_month == 1 and hours == 1 and minutes == 59)):
            p3=1


    if(p3==0): #Everything is normal
        return chain(
            segment_one(p1),
            segment_two(p2),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            silent_wave(),
            beep_wave2()
            )
    elif(p3==2): #Leap second inserted
        return chain(
            segment_one(p1),
            segment_two(p2),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            silent_wave(),
            beep_wave1(),
            beep_wave2()
            )

    elif(p3==1): #Leap second subtracted (Very unlikely!)
        return chain(
            segment_one(p1),
            segment_two(p2),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave1(),
            beep_wave2()
            )



def generate_audio_src_mono(filename, date):
    audio = audio_src(date)
    channels = ((audio, ), (audio, ) )
    samples = compute_samples(channels, None, )
    write_wavefile(filename, samples, None, 1, framerate=44100)


def generate_audio_src_stereo(filename, date):
    audio=audio_src(date)
    channels = ((audio_src(date), ), (audio_src(date), ) )
    samples = compute_samples(channels, None, )
    write_wavefile(filename, samples, None, 2, framerate=44100)
