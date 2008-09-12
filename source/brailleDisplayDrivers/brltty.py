import wx
import braille
try:
	import brlapi
except ImportError:
	pass

KEY_CHECK_INTERVAL = 50

class BrailleDisplayDriver(braille.BrailleDisplayDriverWithCursor):
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
		super(BrailleDisplayDriver, self).__init__()
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

	def _display(self, cells):
		cells = "".join(chr(cell) for cell in cells)
		self._con.writeDots(cells)

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
