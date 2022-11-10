# pySRC
Python library to generate audio signal for [Segnale orario Rai Codificato (SRC)](https://it.wikipedia.org/wiki/Segnale_orario)

### Usage

```
$ python3
Python 3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from datetime import datetime
>>> from pysrc.audio_src import generate_audio_src_stereo
>>> generate_audio_src_stereo('now.wav',datetime.now())
>>>
```
