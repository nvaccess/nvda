#brailleDisplayDrivers/brltty.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2019 NV Access Limited, Babbage B.V>

import time
import wx
import braille
from logHandler import log
import inputCore
from typing import List
try:
	import brlapi
	BRLAPI_CMD_KEYS = {
		code: name[8:].lower()
		for name, code in vars(brlapi).items() if name.startswith("KEY_CMD_")
	}
except ImportError:
	brlapi = None

KEY_CHECK_INTERVAL = 50

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""brltty braille display driver.
	"""
	name = "brltty"
	description = "brltty"

	@classmethod
	def check(cls):
		return bool(brlapi)

	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()
		self._con = brlapi.Connection()
		self._con.enterTtyModeWithPath()
		self._keyCheckTimer = wx.PyTimer(self._handleKeyPresses)
		self._keyCheckTimer.Start(KEY_CHECK_INTERVAL)
		# BRLTTY simulates key presses for braille typing keys, so let BRLTTY handle them.
		# NVDA may eventually implement this itself, but there's no reason to deny BRLTTY users this functionality in the meantime.
		self._con.ignoreKeys(brlapi.rangeType_type, (brlapi.KEY_TYPE_SYM,))

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		# Exceptions might be raised if initialisation failed. Just ignore them.
		try:
			self._keyCheckTimer.Stop()
			self._keyCheckTimer = None
		except:
			pass
		try:
			# Give BRLTTY a chance to write the last piece of data to the display.
			time.sleep(0.05)
			self._con.leaveTtyMode()
		except:
			pass

	def _get_numCells(self):
		return self._con.displaySize[0]

	def display(self, cells: List[int]):
		cells = bytes(cells)
		# HACK: Temporarily work around a bug which causes brltty to freeze if data is written while there are key presses waiting.
		# Simply consume and act upon any waiting key presses.
		self._handleKeyPresses()
		self._con.writeDots(cells)

	def _get_driverName(self):
		return self._con.driverName.decode()

	def _handleKeyPresses(self):
		while True:
			try:
				key = self._con.readKey(False)
			except:
				log.error("Error reading key press from brlapi", exc_info=True)
				return
			if not key:
				break
			key = self._con.expandKeyCode(key)
			self._onKeyPress(key)

	def _onKeyPress(self, key):
		keyType = key["type"]
		command = key["command"]
		argument = key["argument"]
		if keyType == brlapi.KEY_TYPE_CMD:
			try:
				inputCore.manager.executeGesture(
					InputGesture(self.driverName, command, argument)
				)
			except inputCore.NoInputGestureAction:
				pass

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(brltty):fwinlt",),
			"braille_scrollForward": ("br(brltty):fwinrt",),
			"braille_previousLine": ("br(brltty):lnup",),
			"braille_nextLine": ("br(brltty):lndn",),
			"braille_routeTo": ("br(brltty):route",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, command, argument):
		super(InputGesture, self).__init__()
		self.model = model
		self.id = BRLAPI_CMD_KEYS[command]
		if command == brlapi.KEY_CMD_ROUTE:
			self.routingIndex = argument
