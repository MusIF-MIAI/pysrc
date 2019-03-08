from wavebender import sine_wave, compute_samples, write_wavefile
from itertools import chain, islice

from src import generate_packet

import time
from datetime import datetime
import calendar

#Ideated, made and coded by Trainax

HIGH_BIT_FREQ = 2500. #Livello logico 1
LOW_BIT_FREQ = 2000.  #Livello logico 0

BEEP_FREQ = 1000. #Beep di riferimento acustico

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
    p1, p2, avviso =  generate_packet(date)

    anno=date.year
    oggi=date.day
    ora=date.hour
    minuti=date.minute
    mese=date.month

    global p3
    p3=0

    if(avviso != "00"):
        if((avviso == "10" and mese == 1 and oggi == 1 and ora == 0 and minuti == 59) or (avviso == "10" and mese == 7 and oggi == 1 and ora == 1 and minuti == 59)):
            p3=2
        elif((avviso == "11" and mese == 1 and oggi == 1 and ora == 0 and minuti == 59) or (avviso == "11" and mese == 7 and oggi == 1 and ora == 1 and minuti == 59)):
            p3=1


    if(p3==0): #Tutto normale
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
    elif(p3==2): #Minuto da 61 secondi
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

    elif(p3==1): #Minuto da 59 secondi (Molto improbabile!)
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
