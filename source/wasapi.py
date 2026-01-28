# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2025 NV Access Limited, Peter Vagner, Davy Kager, Mozilla Corporation, Google LLC,
# Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import (
	c_void_p,
	cdll,
	CFUNCTYPE,
	c_bool,
	POINTER,
	c_char_p,
	c_wchar_p,
	c_float,
	c_uint,
)
from ctypes.wintypes import (
	DWORD,
	HANDLE,
)
from comtypes import (
	HRESULT,
)
import NVDAState
from winBindings.mmeapi import WAVEFORMATEX


dll = cdll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalDll)

HWasapiPlayer = HANDLE

wasPlay_callback = CFUNCTYPE(None, c_void_p, c_uint)

wasPlay_create = dll.wasPlay_create
wasPlay_create.restype = HWasapiPlayer
wasPlay_create.argtypes = (
	c_wchar_p,  # endpointId
	WAVEFORMATEX,  # format
	wasPlay_callback,  # callback
)

wasPlay_destroy = dll.wasPlay_destroy
wasPlay_destroy.restype = None
wasPlay_destroy.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_open = dll.wasPlay_open
wasPlay_open.restype = HRESULT
wasPlay_open.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_feed = dll.wasPlay_feed
wasPlay_feed.restype = HRESULT
wasPlay_feed.argtypes = (
	HWasapiPlayer,  # player
	c_char_p,  # data
	c_uint,  # size
	POINTER(c_uint),  # id
)

wasPlay_stop = dll.wasPlay_stop
wasPlay_stop.restype = HRESULT
wasPlay_stop.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_sync = dll.wasPlay_sync
wasPlay_sync.restype = HRESULT
wasPlay_sync.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_idle = dll.wasPlay_idle
wasPlay_idle.restype = HRESULT
wasPlay_idle.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_pause = dll.wasPlay_pause
wasPlay_pause.restype = HRESULT
wasPlay_pause.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_resume = dll.wasPlay_resume
wasPlay_resume.restype = HRESULT
wasPlay_resume.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_setChannelVolume = dll.wasPlay_setChannelVolume
wasPlay_setChannelVolume.restype = HRESULT
wasPlay_setChannelVolume.argtypes = (
	HWasapiPlayer,  # player
	c_uint,  # channel
	c_float,  # level
)

wasPlay_startup = dll.wasPlay_startup
wasPlay_startup.restype = HRESULT
wasPlay_startup.argtypes = ()

wasPlay_startTrimmingLeadingSilence = dll.wasPlay_startTrimmingLeadingSilence
wasPlay_startTrimmingLeadingSilence.argtypes = (
	HWasapiPlayer,  # player
	c_bool,  # start
)
wasPlay_startTrimmingLeadingSilence.restype = None

wasSilence_init = dll.wasSilence_init
wasSilence_init.restype = HRESULT
wasSilence_init.argtypes = (
	c_wchar_p,  # endpointId
)

wasSilence_playFor = dll.wasSilence_playFor
wasSilence_playFor.restype = None
wasSilence_playFor.argtypes = (
	DWORD,  # ms
	c_float,  # volume
)

wasSilence_terminate = dll.wasSilence_terminate
wasSilence_terminate.restype = None
wasSilence_terminate.argtypes = ()
