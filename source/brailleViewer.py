#brailleViewer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import gui
import braille
from braille import BrailleDisplayDriver
import inputCore
from logHandler import log

BRAILLE_UNICODE_PATTERNS_START = 0x2800
SPACE_CHARACTER = u" "

class BrailleViewerFrame(wx.MiniFrame):

	def __init__(self, numCells, onCloseFunc):
		super(BrailleViewerFrame, self).__init__(gui.mainFrame, wx.ID_ANY, _("NVDA Braille Viewer"), style=wx.CAPTION | wx.RESIZE_BORDER | wx.STAY_ON_TOP)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.lastBraille = SPACE_CHARACTER * numCells
		self.lastText = SPACE_CHARACTER
		self.onCloseFunc = onCloseFunc
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		item = self.output = wx.StaticText(self, label=self.lastBraille)
		item.Font = self.setFont(item.GetFont(), forBraille=True)
		mainSizer.Add(item, flag=wx.EXPAND)

		item = self.rawoutput = wx.StaticText(self, label=u"hello")
		item.Font = self.setFont(item.Font)
		mainSizer.Add(item, flag=wx.EXPAND)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.Show()

	def updateValues(self, braille, text):
		brailleEqual = self.lastBraille == braille
		textEqual = self.lastText == text
		if brailleEqual and textEqual:
			return
		self.Freeze()
		if not brailleEqual:
			self.output.Label = self.lastBraille = braille
		if not textEqual:
			self.rawoutput.Label = self.lastText = text
		self.Thaw()
		self.Refresh()
		self.Update()

	def setFont(self, font, forBraille=False):
		# Braille characters are much smaller than the raw text characters, override the size
		# I assume this is because the "Courier New" font does not support this unicode range
		# so the system falls back to another font.
		font.PointSize = 20 if not forBraille else 22
		font.Family = wx.FONTFAMILY_TELETYPE
		font.FaceName = "Courier New"
		return font

	def onClose(self, evt):
		self.onCloseFunc()
		if not evt.CanVeto():
			self.Destroy()
			return
		evt.Veto()

DEFAULT_NUM_CELLS = 40

class BrailleViewer(BrailleDisplayDriver):
	name = "brailleViewer"
	description = _("Braille viewer")
	numCells = DEFAULT_NUM_CELLS # Overriden to match an active braille display
	_frame = None

	@classmethod
	def check(cls):
		return True

	def __init__(self, onCloseFunc, numCells=DEFAULT_NUM_CELLS):
		self.numCells = numCells if numCells else DEFAULT_NUM_CELLS
		self.rawText = u""
		self.onCloseFunc = onCloseFunc
		super(BrailleViewer, self).__init__()
		self._setFrame()

	def _setFrame(self):
		# check we have not initialialised yet
		if self._frame:
			return True
		# check the GUI has already initialised.
		if gui.mainFrame:
			self._frame = BrailleViewerFrame(self.numCells, self.onFrameClosed)
		return self._frame is not None

	def display(self, cells):
		if not self._setFrame():
			return
		brailleUnicodeChars = (unichr(BRAILLE_UNICODE_PATTERNS_START + cell) for cell in cells)
		# replace braille "space" with regular space because the width of the braille space
		# does not match the other braille characters, the result is better, but not perfect.
		brailleSpace = unichr(BRAILLE_UNICODE_PATTERNS_START)
		spaceReplaced = (cell.replace(brailleSpace, SPACE_CHARACTER) for cell in brailleUnicodeChars)
		self._frame.updateValues(u"".join(spaceReplaced), self.rawText)

	def onFrameClosed(self):
		self.onCloseFunc()

	def terminate(self):
		super(BrailleViewer, self).terminate()
		try:
			self._frame.Destroy()
			self._frame = None
		except wx.PyDeadObjectError:
			# NVDA's GUI has already terminated.
			pass

