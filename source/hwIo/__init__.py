# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2021 NV Access Limited, Babbage B.V.


"""Raw input/output for braille displays via serial and HID.
See the L{Serial} and L{Hid} classes.
Braille display drivers must be thread-safe to use this, as it utilises a background thread.
See :attr:`braille.display.driver.BrailleDisplayDriver.isThreadSafe`.
"""

from .base import (  # noqa: F401
	IoBase,
	Serial,
	Bulk,
	boolToByte,
	intToByte,
	getByte,
)
from .hid import Hid  # noqa: F401
from .ioThread import IoThread
from . import ble

bgThread: IoThread


def initialize():
	global bgThread
	bgThread = IoThread()
	bgThread.start()
	ble.initialize()


def terminate():
	ble.terminate()
	global bgThread
	bgThread.stop()
	bgThread = None
