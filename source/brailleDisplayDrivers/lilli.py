#brailleDisplayDrivers/lilli.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008 Gianluca Casalino <gianluca.casalino@poste.it>

from ctypes import *
import wx
import braille

try:
	lilliDll=windll.LoadLibrary("brailleDisplayDrivers\\lilli.dll")
except:
	lilliDll=None

lilliCellsMap=[]
KEY_CHECK_INTERVAL = 50

def convertLilliCells(cell):
	newCell = ((1<<6 if cell & 1<<4 else 0) |
		(1<<5 if cell & 1<<5  else 0) |
		(1<<0 if cell & 1<<6  else 0) |
		(1<<3 if cell & 1<<0  else 0) |
		(1<<2 if cell & 1<<1  else 0) |
		(1<<1 if cell & 1<<2  else 0) |
		(1<<7 if cell & 1<<3  else 0) |
		(1<<4 if cell & 1<<7  else 0))
	return newCell

class BrailleDisplayDriver(braille.BrailleDisplayDriverWithCursor):
	name = "lilli"
	description = _("MDV Lilli")

	@classmethod
	def check(cls):
		return bool(lilliDll)

	def  __init__(self):
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

	def _get_numCells(self):
		return 40

	def _handleKeyPresses(self):
		while True:
			try:
				key=lilliDll.ReadBuf()
			except:
				pass
			if not key: break
			if key==11: braille.handler.scrollBack()
			elif key==13: braille.handler.scrollForward()
			elif (key >= 257) and (key <= 296): braille.handler.routeTo(key-257)

	def _display(self, cells):
		cells="".join(chr(lilliCellsMap[x]) for x in cells)
		lilliDll.WriteBuf(create_string_buffer(cells)) 
		self._handleKeyPresses()
