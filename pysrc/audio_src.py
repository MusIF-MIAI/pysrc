from wavebender import sine_wave, compute_samples, write_wavefile
from itertools import chain, islice

from src import generate_packet

HIGH_BIT_FREQ = 2500.
LOW_BIT_FREQ = 2000.

BEEP_FREQ = 1000.

def get_frame(bits):
    wave = None
    for bit in bits:
        data = generate_wave(LOW_BIT_FREQ) if bit == '0' else generate_wave(HIGH_BIT_FREQ)
        wave = data if wave is None else chain(wave, data)
    return wave


def beep_wave():
    return chain(
        generate_wave(BEEP_FREQ, duration=0.1),
        generate_wave(BEEP_FREQ, amplitude=0.000001, duration=0.9)
    )


def silent_wave():
    return generate_wave(BEEP_FREQ, amplitude=0.000001, duration=1)


def generate_wave(frequency=BEEP_FREQ, framerate=44100, amplitude=0.9, duration=0.03):
    return islice(sine_wave(frequency, framerate, amplitude), duration*framerate)


def segment_one(bits):
    return chain(
        get_frame(bits),
        generate_wave(BEEP_FREQ, amplitude=0.000001, duration=0.04)
    )


def segment_two(bits):
    return chain(get_frame(bits), generate_wave(BEEP_FREQ, amplitude=0.000001, duration=0.52))


def audio_src(date):
    p1, p2 =  generate_packet(date)
    return chain(
        segment_one(p1),
        segment_two(p2),
        beep_wave(),
        beep_wave(),
        beep_wave(),
        beep_wave(),
        beep_wave(),
        silent_wave(),
        beep_wave()
    )


def generate_audio_src_mono(filename, date):
    audio = audio_src(date)
    channels = ((audio, ), (audio, ) )
    samples = compute_samples(channels, None, )
    write_wavefile(filename, samples, None, 1, framerate=44100)


def generate_audio_src_stero(date):
    channels = ((audio_src(date), ), (audio_src(date), ) )
    samples = compute_samples(channels, None, )
    write_wavefile(filename, samples, None, 2, framerate=44100)
