import _winreg
import comtypes.client
import braille

COM_CLASS = "HtBrailleDriverServer.HtBrailleDriver"
constants = None

class Sink:
	def onKeysPressed(self, this, keys, routing_pos):
		if constants.KEY_ROUTING in keys:
			braille.handler.routeTo(routing_pos - 1)
		elif constants.KEY_UP in keys:
			braille.handler.scrollBack()
		elif constants.KEY_DOWN in keys:
			braille.handler.scrollForward()

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""HandyTech braille display driver.
	"""
	name = "handyTech"
	description = _("HandyTech braille displays")

	@classmethod
	def check(cls):
		try:
			_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,COM_CLASS).Close()
			return True
		except:
			return False

	def __init__(self):
		global constants
		self._server = comtypes.client.CreateObject(COM_CLASS)
		import comInterfaces.HTBRAILLEDRIVERSERVERLib as constants
		# Keep the connection object so it won't become garbage
		self.advise = comtypes.client.GetEvents(self._server, Sink())
		self._server.initialize()
		self._cursorShape = 0xc0
		self._cursorBlinkRate = 1000
		self._server.configureCursor(self._cursorBlinkRate, self._cursorShape)

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		self._server.terminate()

	def _get_numCells(self):
		return self._server.getCurrentTextLength()[0]

	def display(self, cells):
		self._server.displayText(cells)

	def _set_cursorPos(self, pos):
		if pos is None:
			self._server.enableCursor(False)
		else:
			self._server.enableCursor(True)
			self._server.setCursorPos(pos + 1)

	def _get_cursorShape(self):
		return self._cursorShape

	def _set_cursorShape(self, shape):
		self._cursorShape = shape
		self._server.configureCursor(self._cursorBlinkRate, self._cursorShape)

	def _get_cursorBlinkRate(self):
		return self._cursorBlinkRate

	def _set_cursorBlinkRate(self, rate):
		self._cursorBlinkRate = rate
		self._server.configureCursor(self._cursorBlinkRate, self._cursorShape)
