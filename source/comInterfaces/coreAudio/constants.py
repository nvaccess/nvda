# This file is a part of pycaw library (https://github.com/AndreMiras/pycaw).
# Please note that it is distributed under MIT license:
# https://github.com/AndreMiras/pycaw#MIT-1-ov-file

from enum import Enum, IntEnum

from comtypes import GUID

IID_Empty = GUID("{00000000-0000-0000-0000-000000000000}")

CLSID_MMDeviceEnumerator = GUID("{BCDE0395-E52F-467C-8E3D-C4579291692E}")


class ERole(Enum):
	eConsole = 0
	eMultimedia = 1
	eCommunications = 2
	ERole_enum_count = 3


class EDataFlow(Enum):
	eRender = 0
	eCapture = 1
	eAll = 2
	EDataFlow_enum_count = 3


class DEVICE_STATE(Enum):
	ACTIVE = 0x00000001
	DISABLED = 0x00000002
	NOTPRESENT = 0x00000004
	UNPLUGGED = 0x00000008
	MASK_ALL = 0x0000000F


class AudioDeviceState(Enum):
	Active = 0x1
	Disabled = 0x2
	NotPresent = 0x4
	Unplugged = 0x8


class STGM(Enum):
	STGM_READ = 0x00000000


class AUDCLNT_SHAREMODE(Enum):
	AUDCLNT_SHAREMODE_SHARED = 0x00000001
	AUDCLNT_SHAREMODE_EXCLUSIVE = 0x00000002


class AudioSessionState(IntEnum):
	# IntEnum to make instances comparable.
	Inactive = 0
	Active = 1
	Expired = 2




