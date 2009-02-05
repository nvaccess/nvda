import _winreg
import comtypes.client
import braille
from logHandler import log

COM_CLASS = "HtBrailleDriverServer.HtBrailleDriver"
constants = None

class Sink:
	def onKeysPressed(self, keys_arg, routing_pos):
		# keys_arg is VARIANT. Indexing by 0 gives actual value.
		keys = keys_arg[0]
		if constants.KEY_ROUTING in keys:
			braille.handler.routeTo(routing_pos - 1)
		elif constants.KEY_UP in keys:
			braille.handler.scrollBack()
		elif constants.KEY_DOWN in keys:
			braille.handler.scrollForward()

class BrailleDisplayDriver(braille.BrailleDisplayDriverWithCursor):
	"""Handy Tech braille display driver.
	"""
	name = "handyTech"
	description = _("Handy Tech braille displays")

	@classmethod
	def check(cls):
		try:
			_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,COM_CLASS).Close()
			return True
		except:
			return False

	def __init__(self):
		global constants
		super(BrailleDisplayDriver, self).__init__()
		self._server = comtypes.client.CreateObject(COM_CLASS)
		import comtypes.gen.HTBRAILLEDRIVERSERVERLib as constants
		# Keep the connection object so it won't become garbage
		self.advise = comtypes.client.GetEvents(self._server, Sink())
		self._server.initialize()

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		self._server.terminate()

	def _get_numCells(self):
		return self._server.getCurrentTextLength()[0]

	def _display(self, cells):
		self._server.displayText(cells)
