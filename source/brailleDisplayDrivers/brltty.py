# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2023 NV Access Limited, Babbage B.V, Bram Duvigneau

import os
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

# BRLAPI named pipes for local connections are numbered and all start with a common name.
# This name is set on compile time and should be the same for all BRLTTY releases,
# however, if a user compiles their own version this may differ
BRLAPI_NAMED_PIPE_PREFIX = "BrlAPI"

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""brltty braille display driver.
	"""
	name = "brltty"
	description = "brltty"
	isThreadSafe = True

	# Type info for auto property: _get_brlapi_pipes
	brlapi_pipes: List[str]

	@classmethod
	def _get_brlapi_pipes(cls) -> List[str]:
		"""Get the BrlAPI named pipes

		Every BRLTTY instance with the BrlAPI enabled will have it's own named pipe to accept API connections.
		The brlapi.Connection constructor takes either a `host:port` argument or just `:port`.
		If only a port is given, this corresponds to the number at the end of the named pipe.
		"""
		return [pipe.name for pipe in os.scandir("//./pipe/") if pipe.name.startswith(BRLAPI_NAMED_PIPE_PREFIX)]

	@classmethod
	def check(cls):
		if not bool(brlapi):
			return False
		# Since this driver only supports local connections for now,
		# we can mark it as unavailable if there are no BrlAPI named pipes present
		return bool(cls.brlapi_pipes)

	def __init__(self):
		super().__init__()
		self._con = brlapi.Connection()
		self._con.enterTtyModeWithPath()
		self._keyCheckTimer = wx.PyTimer(self._handleKeyPresses)
		self._keyCheckTimer.Start(KEY_CHECK_INTERVAL)
		# BRLTTY simulates key presses for braille typing keys, so let BRLTTY handle them.
		# NVDA may eventually implement this itself, but there's no reason to deny BRLTTY users this functionality in the meantime.
		self._con.ignoreKeys(brlapi.rangeType_type, (brlapi.KEY_TYPE_SYM,))

	def terminate(self):
		super().terminate()
		# Exceptions might be raised if initialisation failed. Just ignore them.
		try:
			self._keyCheckTimer.Stop()
			self._keyCheckTimer = None
		except:  # noqa: E722
			pass
		try:
			# Give BRLTTY a chance to write the last piece of data to the display.
			time.sleep(0.05)
			self._con.leaveTtyMode()
		except:  # noqa: E722
			pass

	def _get_numCols(self) -> int:
		return self._con.displaySize[0]
	
	def _get_numRows(self) -> int:
		return self._con.displaySize[1]

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
			except:  # noqa: E722
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
			"toggleInputHelp": ("br(brltty):learn"),
			"showGui": ("br(brltty):prefmenu",),
			"revertConfiguration": ("br(brltty):prefload",),
			"saveConfiguration": ("br(brltty):prefsave",),
			"dateTime": ("br(brltty):time",),
			"review_currentLine": ("br(brltty):say_line",),
			"review_sayAll": ("br(brltty):say_below",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, command, argument):
		super().__init__()
		self.model = model
		self.id = BRLAPI_CMD_KEYS[command]
		if command == brlapi.KEY_CMD_ROUTE:
			self.routingIndex = argument
