import wx
import braille
try:
	import brlapi
except ImportError:
	pass

KEY_CHECK_INTERVAL = 50

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""brltty braille display driver.
	"""
	name = "brltty"
	description = "brltty"

	@classmethod
	def check(cls):
		try:
			c = brlapi.Connection()
			del c
			return True
		except:
			pass
		return False

	def __init__(self):
		self._con = brlapi.Connection()
		self._con.enterTtyModeWithPath()
		self._keyCheckTimer = wx.PyTimer(self._handleKeyPresses)
		self._keyCheckTimer.Start(KEY_CHECK_INTERVAL)

	def __del__(self):
		# Exceptions might be raised if initialisation failed. Just ignore them.
		try:
			self._keyCheckTimer.Stop()
		except:
			pass
		try:
			self._con.leaveTtyMode()
		except:
			pass

	def _get_numCells(self):
		return self._con.displaySize[0]

	def display(self, cells):
		self._cells = cells
		self._display()

	def _display(self):
		# The string sent to the display needs to be the length of the display, so pad with zeroes if necessary.
		out = "".join(chr(cell) for cell in self._cells) + "\0" * (self.numCells - len(self._cells))
		self._con.writeDots(out)

	def _handleKeyPresses(self):
		while True:
			key = self._con.readKey(False)
			if not key:
				break
			key = self._con.expandKeyCode(key)
			self._onKeyPress(key)

	def _onKeyPress(self, key):
		keyType = key["type"]
		command = key["command"]
		argument = key["argument"]
		if keyType == brlapi.KEY_TYPE_CMD:
			if command == brlapi.KEY_CMD_FWINLT:
				braille.handler.buffer.scrollBack()
			elif command == brlapi.KEY_CMD_FWINRT:
				braille.handler.buffer.scrollForward()
			elif command == brlapi.KEY_CMD_ROUTE:
				braille.handler.buffer.routeTo(argument)
