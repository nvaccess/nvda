# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2026 NV Access Limited, Babbage B.V.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


"""Raw input/output for braille displays via serial and HID.
See the L{Serial} and L{Hid} classes.
Braille display drivers must be thread-safe to use this, as it utilises a background thread.
See L{braille.BrailleDisplayDriver.isThreadSafe}.
"""

from .base import (  # noqa: F401, I001
	IoBase,
	Serial,
	Bulk,
	boolToByte,
	intToByte,
	getByte,
)
from .hid import Hid  # noqa: F401
from .ioThread import IoThread

bgThread: IoThread


def initialize():
	global bgThread
	bgThread = IoThread()
	bgThread.start()
	from . import ble

	ble.initialize()


def terminate():
	from . import ble

	ble.terminate()
	global bgThread
	bgThread.stop()
	bgThread = None
