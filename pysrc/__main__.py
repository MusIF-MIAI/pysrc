from datetime import datetime

from audio_src import generate_audio_src_mono


now = datetime.now()
generate_audio_src_mono('now.wav', now)
