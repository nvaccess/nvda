# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2026 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Wrapper for the winEventLimiter dll,
which registers for winEvents and limits them on a dedicated thread,
outside of NVDA's core (Python) event loop.

.. seealso::
	``nvdaHelper/winEventLimiter``
"""

import ctypes
from ctypes import wintypes

import NVDAState


class EventData(ctypes.Structure):
	"""A single winEvent, as collected by the winEventLimiter dll.

	.. seealso::
		``nvdaHelper/winEventLimiter/lib/eventData.h``
	"""

	_fields_ = (
		("idEvent", wintypes.DWORD),
		("hwnd", wintypes.HWND),
		("idObject", wintypes.LONG),
		("idChild", wintypes.LONG),
		("dwEventThread", wintypes.DWORD),
		("dwmsEventTime", wintypes.DWORD),
		("bypassesPreprocessing", ctypes.c_bool),
	)


NotifyCallback = ctypes.CFUNCTYPE(None, ctypes.c_int)
"""Function called by the winEventLimiter dll when new events are available to fetch.
The argument is non-zero when the new events include a focus event,
so the client can pump immediately rather than after a delay (#14928).
"""


def getWinEventLimiterDll() -> ctypes.CDLL:
	"""Load the winEventLimiter dll and configure its function prototypes.

	:raises OSError: If the dll could not be loaded.
	:return: The loaded dll.
	"""
	dll = ctypes.cdll.LoadLibrary(NVDAState.ReadPaths.winEventLimiterDll)

	dll.winEventLimiter_getEvents.restype = ctypes.c_uint
	dll.winEventLimiter_getEvents.argtypes = (
		ctypes.c_uint,  # eventIndex
		ctypes.c_uint,  # maxEvents
		ctypes.POINTER(EventData),  # data
	)

	dll.winEventLimiter_getEventCount.restype = ctypes.c_uint
	dll.winEventLimiter_getEventCount.argtypes = ()

	dll.winEventLimiter_flushDestroyEvents.restype = None
	dll.winEventLimiter_flushDestroyEvents.argtypes = ()

	dll.winEventLimiter_getDestroyEvents.restype = ctypes.c_uint
	dll.winEventLimiter_getDestroyEvents.argtypes = (
		ctypes.c_uint,  # eventIndex
		ctypes.c_uint,  # maxEvents
		ctypes.POINTER(EventData),  # data
	)

	dll.winEventLimiter_getDestroyEventCount.restype = ctypes.c_uint
	dll.winEventLimiter_getDestroyEventCount.argtypes = ()

	dll.winEventLimiter_takeLostDestroys.restype = ctypes.c_int
	dll.winEventLimiter_takeLostDestroys.argtypes = ()

	dll.winEventLimiter_flushEvents.restype = ctypes.c_int
	dll.winEventLimiter_flushEvents.argtypes = ()

	dll.winEventLimiter_start.restype = ctypes.c_int
	dll.winEventLimiter_start.argtypes = (
		NotifyCallback,  # notifyOfNewEventsCallback
		ctypes.POINTER(wintypes.DWORD),  # eventIds
		ctypes.c_uint,  # eventIdCount
	)

	dll.winEventLimiter_stop.restype = ctypes.c_int
	dll.winEventLimiter_stop.argtypes = ()

	dll.winEventLimiter_addEvent.restype = ctypes.c_int
	dll.winEventLimiter_addEvent.argtypes = (
		wintypes.DWORD,  # eventID
		wintypes.HWND,  # window
		wintypes.LONG,  # objectID
		wintypes.LONG,  # childID
		wintypes.DWORD,  # threadID
	)

	dll.winEventLimiter_setAlwaysAllowedObject.restype = ctypes.c_int
	dll.winEventLimiter_setAlwaysAllowedObject.argtypes = (
		wintypes.HWND,  # hwnd
		wintypes.LONG,  # idObject
		wintypes.LONG,  # idChild
	)

	dll.winEventLimiter_getConsoleThreadID.restype = wintypes.DWORD
	dll.winEventLimiter_getConsoleThreadID.argtypes = (
		wintypes.HWND,  # hwnd
	)

	return dll
