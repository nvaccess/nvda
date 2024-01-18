# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from ctypes import POINTER, Structure, c_float
from ctypes.wintypes import BOOL, UINT

from comtypes import GUID


class AUDIO_VOLUME_NOTIFICATION_DATA(Structure):
	_fields_ = [
		("guidEventContext", GUID),
		("bMuted", BOOL),
		("fMasterVolume", c_float),
		("nChannels", UINT),
		("afChannelVolumes", c_float * 8),
	]


PAUDIO_VOLUME_NOTIFICATION_DATA = POINTER(AUDIO_VOLUME_NOTIFICATION_DATA)



