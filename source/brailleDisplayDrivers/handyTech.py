#brailleDisplayDrivers/handyTech.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _winreg
import comtypes.client
import braille
from logHandler import log
import speech

COM_CLASS = "HtBrailleDriverServer.HtBrailleDriver"
constants = None

class Sink:

	def __init__(self, server):
		self.server = server

	def sayString(self, text):
		speech.speakMessage(text)

	def onKeysPressed(self, keys_arg, routing_pos):
		# keys_arg is VARIANT. Indexing by 0 gives actual value.
		keys = keys_arg[0]
		if constants.KEY_ROUTING in keys:
			braille.handler.routeTo(routing_pos - 1)
		elif keys == (constants.KEY_UP,) or keys == (constants.KEY_LEFT,):
			braille.handler.scrollBack()
		elif keys == (constants.KEY_DOWN,) or keys == (constants.KEY_RIGHT,):
			braille.handler.scrollForward()
		elif keys == (constants.KEY_B4, constants.KEY_B8):
			self.server.startConfigDialog(False)

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
		self._advise = comtypes.client.GetEvents(self._server, Sink(self._server), constants.IHtBrailleDriverSink)
		self._server.initialize()

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		self._server.terminate()

	def _get_numCells(self):
		return self._server.getCurrentTextLength()[0]

	def _display(self, cells):
		self._server.displayText(cells)
