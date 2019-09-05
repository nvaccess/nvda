# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2026 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Wrapper for the eventHandler dll,
which registers for winEvents and limits them on a dedicated thread,
outside of NVDA's core (Python) event loop.

.. seealso::
	``nvdaHelper/eventHandler``
"""

import ctypes
from ctypes import wintypes

import NVDAState


class EventData(ctypes.Structure):
	"""A single winEvent, as collected by the eventHandler dll.

	.. seealso::
		``nvdaHelper/eventHandler/eventHandler_lib/eventData.h``
	"""

	_fields_ = (
		("idEvent", wintypes.DWORD),
		("hwnd", wintypes.HWND),
		("idObject", wintypes.LONG),
		("idChild", wintypes.LONG),
		("dwEventThread", wintypes.DWORD),
		("dwmsEventTime", wintypes.DWORD),
	)


NotifyCallback = ctypes.CFUNCTYPE(None)
"""Function called by the eventHandler dll when new events are available to fetch."""

ObjectDestroyedCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(EventData))
"""Function called by the eventHandler dll when an object destroy winEvent is received."""


def getEventHandlerDll() -> ctypes.CDLL:
	"""Load the eventHandler dll and configure its function prototypes.

	:raises OSError: If the dll could not be loaded.
	:return: The loaded dll.
	"""
	dll = ctypes.cdll.LoadLibrary(NVDAState.ReadPaths.eventHandlerDll)

	dll.GetEvents.restype = ctypes.c_uint
	dll.GetEvents.argtypes = (
		ctypes.c_uint,  # eventIndex
		ctypes.c_uint,  # maxEvents
		ctypes.POINTER(EventData),  # data
	)

	dll.GetEventCount.restype = ctypes.c_uint
	dll.GetEventCount.argtypes = ()

	dll.FlushEvents.restype = None
	dll.FlushEvents.argtypes = ()

	dll.RegisterAndPump_Async.restype = ctypes.c_int
	dll.RegisterAndPump_Async.argtypes = (
		NotifyCallback,  # notifyOfNewEventsCallback
		ObjectDestroyedCallback,  # notifyOfDestroyEventCallback
	)

	dll.RegisterAndPump_Join.restype = ctypes.c_int
	dll.RegisterAndPump_Join.argtypes = ()

	return dll
