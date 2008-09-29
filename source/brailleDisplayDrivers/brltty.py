import wx
import braille
from logHandler import log
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
		# HACK: Temporarily work around a bug which causes brltty to freeze if data is written while there are key presses waiting.
		# Simply consume and act upon any waiting key presses.
		self._handleKeyPresses()
		self._con.writeDots(cells)

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
		try:
			if keyType == brlapi.KEY_TYPE_CMD:
				if command == brlapi.KEY_CMD_FWINLT:
					braille.handler.buffer.scrollBack()
				elif command == brlapi.KEY_CMD_FWINRT:
					braille.handler.buffer.scrollForward()
				elif command == brlapi.KEY_CMD_ROUTE:
					braille.handler.buffer.routeTo(argument)
		except:
			log.error("Error executing key press action", exc_info=True)
