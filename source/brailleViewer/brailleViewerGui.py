from typing import List

import wx
import gui
import config
from logHandler import log

BRAILLE_UNICODE_PATTERNS_START = 0x2800
SPACE_CHARACTER = u" "


# Inherit from wx.Frame because these windows show in the alt+tab menu (where miniFrame does not)
# wx.Dialog causes a crash on destruction when multiple were created at the same time (speechViewer
# may start at the same time)
class BrailleViewerFrame(wx.Frame):

	# Translators: The title of the NVDA Braille Viewer tool window.
	title = _("NVDA Braille Viewer")

	def __init__(self, numCells, onDestroyed):
		dialogPos = wx.DefaultPosition
		if not config.conf["brailleViewer"]["autoPositionWindow"] and self.doDisplaysMatchConfig():
			log.debug("Setting brailleViewer window position")
			brailleViewSection = config.conf["brailleViewer"]
			dialogPos = wx.Point(x=brailleViewSection["x"], y=brailleViewSection["y"])
		super(BrailleViewerFrame, self).__init__(
			gui.mainFrame,
			title=self.title,
			pos=dialogPos,
			style=wx.CAPTION | wx.STAY_ON_TOP
		)
		self._notifyOfDestroyed = onDestroyed
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
		self.lastBraille = SPACE_CHARACTER * numCells
		self.lastText = SPACE_CHARACTER
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		item = self.output = wx.StaticText(self, label=self.lastBraille)
		item.Font = self.setFont(item.GetFont(), forBraille=True)
		mainSizer.Add(item, flag=wx.EXPAND)

		item = self.rawoutput = wx.StaticText(self, label=SPACE_CHARACTER)
		item.Font = self.setFont(item.Font)
		mainSizer.Add(item, flag=wx.EXPAND)

		# Translators: The label for a setting in the braille viewer that controls
		# whether the braille viewer is shown at startup or not.
		showOnStartupCheckboxLabel = _("&Show Braille Viewer on Startup")
		self.shouldShowOnStartupCheckBox = wx.CheckBox(
			parent=self,
			label=showOnStartupCheckboxLabel)
		self.shouldShowOnStartupCheckBox.SetValue(config.conf["brailleViewer"]["showBrailleViewerAtStartup"])
		self.shouldShowOnStartupCheckBox.Bind(wx.EVT_CHECKBOX, self.onShouldShowOnStartupChanged)
		mainSizer.Add(self.shouldShowOnStartupCheckBox, border=5, flag=wx.ALL)

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.ShowWithoutActivating()

	def onShouldShowOnStartupChanged(self, evt):
		config.conf["brailleViewer"]["showBrailleViewerAtStartup"] = self.shouldShowOnStartupCheckBox.IsChecked()

	def doDisplaysMatchConfig(self):
		configSizes = config.conf["brailleViewer"]["displays"]
		attachedSizes = self.getAttachedDisplaySizesAsStringArray()
		lengthsMatch = len(configSizes) == len(attachedSizes)
		allSizesMatch = all(
			confSize == attachedSize
			for (confSize, attachedSize)
			in zip(configSizes, attachedSizes)
		)
		return lengthsMatch and allSizesMatch

	def updateBrailleDisplayed(
			self,
			cells: List[int],
			rawText: str = u""
	):
		if self.isDestroyed:
			return
		brailleUnicodeChars = (chr(BRAILLE_UNICODE_PATTERNS_START + cell) for cell in cells)
		# replace braille "space" with regular space because the width of the braille space
		# does not match the other braille characters, the result is better, but not perfect.
		brailleSpace = chr(BRAILLE_UNICODE_PATTERNS_START)
		spaceReplaced = (
			cell.replace(brailleSpace, SPACE_CHARACTER)
			for cell in brailleUnicodeChars
		)
		braille = u"".join(spaceReplaced)

		brailleEqual = self.lastBraille == braille
		textEqual = self.lastText == rawText
		if brailleEqual and textEqual:
			return
		self.Freeze()
		if not brailleEqual:
			self.output.Label = self.lastBraille = braille
		if not textEqual:
			self.rawoutput.Label = self.lastText = rawText
		self.Thaw()
		self.Refresh()
		self.Update()

	def setFont(self, font, forBraille=False):
		# We would like the raw characters to align with the braille dots, however, the
		# Braille characters are much smaller than the raw text characters so we override the size
		# to make them closer. It is still not an exact match.
		# I assume this is because the "Courier New" font does not support this unicode range
		# so the system falls back to another font.
		font.PointSize = 20 if not forBraille else 22
		font.Family = wx.FONTFAMILY_TELETYPE
		font.FaceName = "Courier New"
		return font

	def getAttachedDisplaySizesAsStringArray(self):
		displays = (
			wx.Display(i).GetGeometry().GetSize()
			for i in range(wx.Display.GetCount())
		)
		return [
			repr((disp.width, disp.height))
			for disp in displays
		]

	def savePositionInformation(self):
		log.debug("Save braille viewer position info")
		position = self.GetPosition()
		config.conf["brailleViewer"]["x"] = position.x
		config.conf["brailleViewer"]["y"] = position.y
		config.conf["brailleViewer"]["displays"] = self.getAttachedDisplaySizesAsStringArray()
		config.conf["brailleViewer"]["autoPositionWindow"] = False

	isDestroyed: bool = False

	def onClose(self, evt):
		log.debug("braille viewer gui onclose")
		if not evt.CanVeto():
			self.isDestroyed = True
			self.Destroy()
			return
		evt.Veto()

	def onDestroy(self, evt):
		log.debug("braille viewer gui destroyed")
		self.savePositionInformation()
		self.isDestroyed = True
		self._notifyOfDestroyed()
		evt.Skip()
