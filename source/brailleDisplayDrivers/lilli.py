#brailleDisplayDrivers/lilli.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2017 NV Access Limited, Gianluca Casalino, Alberto Benassati, Babbage B.V.
from typing import Optional, List

import os
import globalVars
from logHandler import log
from ctypes import windll
import inputCore
import wx
import braille

try:
	lilliDll = windll.LoadLibrary(os.path.join(globalVars.appDir, "brailleDisplayDrivers", "lilli.dll"))
except:
	lilliDll=None

lilliCellsMap: List[int] = []
KEY_CHECK_INTERVAL = 50

LILLI_KEYS = [
	"", "F1", "F2", "F3", "F4",  "F5", "F6", "F7", "F8", "F9", "F10", "LF", "UP", "RG", "DN", "",
	"", "SF1", "SF2", "SF3", "SF4",  "SF5", "SF6", "SF7", "SF8", "SF9", "SF10", "SLF", "SUP", "SRG", "SDN", "",
	"", "LF1", "LF2", "LF3", "LF4",  "LF5", "LF6", "LF7", "LF8", "LF9", "LF10", "LLF", "LUP", "LRG", "LDN", "",
	"", "SLF1", "SLF2", "SLF3", "SLF4",  "SLF5", "SLF6", "SLF7", "SLF8", "SLF9", "SLF10", "SLLF", "SLUP", "SLRG", "SLDN", "SFDN", "SFUP",
	"route"
]
ROUTE_COMMAND = "route"

def convertLilliCells(cell: int) -> int:
	newCell = (
			(1<<6 if cell & 1<<4 else 0) |
			(1<<5 if cell & 1<<5 else 0) |
			(1<<0 if cell & 1<<6 else 0) |
			(1<<3 if cell & 1<<0 else 0) |
			(1<<2 if cell & 1<<1 else 0) |
			(1<<1 if cell & 1<<2 else 0) |
			(1<<7 if cell & 1<<3 else 0) |
			(1<<4 if cell & 1<<7 else 0)
	)
	return newCell

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "lilli"
	# Translators: Name of a braille display.
	description = _("MDV Lilli")

	@classmethod
	def check(cls):
		return bool(lilliDll)

	def __init__(self):
		global lilliCellsMap
		super(BrailleDisplayDriver, self).__init__()
		lilliCellsMap=[convertLilliCells(x) for x in range(256)]
		if (lilliDll.Init408USB()):
			self._keyCheckTimer = wx.PyTimer(self._handleKeyPresses)
			self._keyCheckTimer.Start(KEY_CHECK_INTERVAL)
		else:
			raise RuntimeError("No display found")

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		try:
			self._keyCheckTimer.Stop()
			self._keyCheckTimer = None
		except:
			pass
		lilliDll.Close408USB()

	def _get_numCells(self) -> int:
		return 40

	def _handleKeyPresses(self):
		while True:
			key: Optional[int] = None
			try:
				# Python 3: review required
				# The code seems to assume this returns an int.
				# I haven't confirmed this.
				key = lilliDll.ReadBuf()
			except:
				log.debug("", exc_info=True)
				pass
			if not key:
				break
			if (key <= 0x40) or (0x101 <= key <= 0x128):
				self._onKeyPress(key)

	def _onKeyPress(self, key: int):
		try:
			if 0x101 <= key <= 0x128:
				inputCore.manager.executeGesture(InputGesture(ROUTE_COMMAND, key - 0x101))
			elif key <= 0x40:
				inputCore.manager.executeGesture(InputGesture(LILLI_KEYS[key], 0))
		except inputCore.NoInputGestureAction:
			pass

	def display(self, cells: List[int]):
		lilliDll.WriteBuf(bytes(lilliCellsMap[x] for x in cells))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(lilli):route",),
			"braille_scrollBack": ("br(lilli):LF",),
			"braille_previousLine": ("br(lilli):UP",),
			"braille_nextLine": ("br(lilli):DN",),
			"braille_scrollForward": ("br(lilli):RG",),			
			"kb:shift+tab": ("br(lilli):SLF",),
			"kb:tab": ("br(lilli):SRG",),
			"kb:alt+tab": ("br(lilli):SDN",),
			"kb:alt+shift+tab": ("br(lilli):SUP",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, command: str, argument: int):
		super(InputGesture, self).__init__()
		self.id = command
		if command == ROUTE_COMMAND:
			self.routingIndex = argument
