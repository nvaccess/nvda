# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import Structure
from ctypes.wintypes import WORD


class WAVEFORMATEX(Structure):
    _fields_ = [
        ("wFormatTag", WORD),
        ("nChannels", WORD),
        ("nSamplesPerSec", WORD),
        ("nAvgBytesPerSec", WORD),
        ("nBlockAlign", WORD),
        ("wBitsPerSample", WORD),
        ("cbSize", WORD),
    ]
