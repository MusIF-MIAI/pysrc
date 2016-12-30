# pySRC
Python library to generate audio signal for [Segnale orario Rai Codificato (SRC)](http://www.inrim.it/res/tf/src_i.shtml)

### Usage

```
$ python 
Python 2.7.13rc1 (default, Dec  4 2016, 14:12:39) 
[GCC 6.2.1 20161124] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from datetime import datetime
>>> from pysrc.audio_src import generate_audio_src_mono
>>> generate_audio_src_mono('now.wav', datetime.now())
>>> 
```
