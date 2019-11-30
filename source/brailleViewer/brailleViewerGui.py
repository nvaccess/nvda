# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from typing import List

import wx
import gui
import config
from logHandler import log
import fonts

BRAILLE_UNICODE_PATTERNS_START = 0x2800
BRAILLE_SPACE_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START)
BRAILLE_INIT_CHARACTER = BRAILLE_SPACE_CHARACTER
SPACE_CHARACTER = u" "


# Inherit from wx.Frame because these windows show in the alt+tab menu (where miniFrame does not)
# wx.Dialog causes a crash on destruction when multiple were created at the same time (speechViewer
# may start at the same time)
class BrailleViewerFrame(wx.Frame):

	# Translators: The title of the NVDA Braille Viewer tool window.
	_title = _("NVDA Braille Viewer")
	_numCells: int
	_rawTextOutputLastSet: str
	_rawTextOutput: wx.StaticText
	_brailleOutputLastSet: str
	_brailleOutput: wx.StaticText
	_shouldShowOnStartupCheckBox: wx.CheckBox

	def __init__(self, numCells, onDestroyed):
		log.debug(f"Starting braille viewer with {numCells} cells")

		dialogPos = wx.DefaultPosition
		if not config.conf["brailleViewer"]["autoPositionWindow"] and self._doDisplaysMatchConfig():
			log.debug("Setting brailleViewer window position")
			brailleViewSection = config.conf["brailleViewer"]
			dialogPos = wx.Point(x=brailleViewSection["x"], y=brailleViewSection["y"])

		super(BrailleViewerFrame, self).__init__(
			gui.mainFrame,
			title=self._title,
			pos=dialogPos,
			style=wx.CAPTION | wx.STAY_ON_TOP
		)
		self.Bind(wx.EVT_CLOSE, self._onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy)

		self._notifyOfDestroyed = onDestroyed
		self._numCells = numCells
		self._brailleOutputLastSet = BRAILLE_INIT_CHARACTER * numCells
		self._rawTextOutputLastSet = SPACE_CHARACTER

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		borderSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(
			borderSizer,
			proportion=1,
			flag=wx.EXPAND | wx.ALL,
			border=5,
		)
		self._brailleOutput = wx.StaticText(self, label=self._brailleOutputLastSet)
		self._brailleOutput.Font = self._setBrailleFont(self._brailleOutput.GetFont())
		log.debug(f"Font for braille: {self._brailleOutput.Font.GetNativeFontInfoUserDesc()}")
		borderSizer.Add(self._brailleOutput, flag=wx.EXPAND, proportion=1)

		self._rawTextOutput = wx.StaticText(self, label=self._rawTextOutputLastSet)
		self._rawTextOutput.Font = self._setRawTextFont(self._rawTextOutput.Font)
		log.debug(f"Font for raw text: {self._rawTextOutput.Font.GetNativeFontInfoUserDesc()}")
		borderSizer.Add(self._rawTextOutput, flag=wx.EXPAND, proportion=1)

		# Translators: The label for a setting in the braille viewer that controls
		# whether the braille viewer is shown at startup or not.
		showOnStartupCheckboxLabel = _("&Show Braille Viewer on Startup")
		self._shouldShowOnStartupCheckBox = wx.CheckBox(
			parent=self,
			label=showOnStartupCheckboxLabel)
		self._shouldShowOnStartupCheckBox.SetValue(config.conf["brailleViewer"]["showBrailleViewerAtStartup"])
		self._shouldShowOnStartupCheckBox.Bind(wx.EVT_CHECKBOX, self._onShouldShowOnStartupChanged)
		borderSizer.AddSpacer(5)
		borderSizer.Add(self._shouldShowOnStartupCheckBox)

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.ShowWithoutActivating()

	def _onShouldShowOnStartupChanged(self, evt):
		config.conf["brailleViewer"]["showBrailleViewerAtStartup"] = self._shouldShowOnStartupCheckBox.IsChecked()

	def _doDisplaysMatchConfig(self):
		configSizes = config.conf["brailleViewer"]["displays"]
		attachedSizes = self._getAttachedDisplaySizesAsStringArray()
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
			rawText: str,
			currentCellCount: int,
	):
		if self.isDestroyed:
			return
		self._numCells = currentCellCount
		adjustOffsetsToUnicode = [
			chr(BRAILLE_UNICODE_PATTERNS_START + cell)
			for cell in cells
		]
		# Create a unicode string that is at least as long as expected.
		# A later call to `Fit` will ensure that strings that are too long are handled.
		padToLen = self._numCells + 2  # Ensure all content is displayed, append 2 extra space characters
		braille = u"".join(adjustOffsetsToUnicode).ljust(padToLen, BRAILLE_SPACE_CHARACTER)

		# Determine what we must update
		brailleEqual = self._brailleOutputLastSet == braille
		textEqual = self._rawTextOutputLastSet == rawText
		if brailleEqual and textEqual:
			# Exit early if we do not have to update either label.
			return

		# Update the GUI
		# Freeze so that we don't see flickering while updates take place.
		self.Freeze()
		if not brailleEqual:
			self._brailleOutput.Label = self._brailleOutputLastSet = braille
		if not textEqual:
			self._rawTextOutput.Label = self._rawTextOutputLastSet = rawText

		# Ensure that any variation in the number of characters displayed is still shown by calling `Fit`.
		# This should really only happen when an external display with a different cell count is connected.
		# If there is some other reason, it is better for the window size to adjust, than to miss content.
		self.Fit()
		self.Thaw()
		self.Refresh()
		self.Update()

	def _setBrailleFont(self, font: wx.Font) -> wx.Font:
		fonts.importFonts()
		fontName = "FreeMono-FixedBraille"
		# Ideally the raw characters should align with the braille dots.
		#
		# On most systems, it seems that Windows will fall back to using "Segoe UI Symbol" font.
		# The width of BRAILLE_SPACE_CHARACTER ('no pins up') does not match the other braille characters.
		# This causes variations in the length of the braille text, particularly when the cursor is flashing.
		# The other disadvantage of using this font is that it is difficult to get its width to match the width
		# of the raw text characters.
		# These issues are solved by using a custom font (FreeMono-FixedBraille), which due to its free (GPL 3)
		# status, allowed us to modify it, and fix the visual issues that it also had.
		#
		# Remaining visual issues:
		# Some words when translated to braille have more characters than the raw text.
		# This may be because there is a leading "number" or "capital letter" cell.
		# Currently we do not handle this.
		font.SetPointSize(20)
		font.SetFaceName(fontName)
		return font

	def _setRawTextFont(self, font: wx.Font) -> wx.Font:
		return self._setBrailleFont(font)

	def _getAttachedDisplaySizesAsStringArray(self):
		displays = (
			wx.Display(i).GetGeometry().GetSize()
			for i in range(wx.Display.GetCount())
		)
		return [
			repr((disp.width, disp.height))
			for disp in displays
		]

	def _savePositionInformation(self):
		log.debug("Save braille viewer position info")
		position = self.GetPosition()
		config.conf["brailleViewer"]["x"] = position.x
		config.conf["brailleViewer"]["y"] = position.y
		config.conf["brailleViewer"]["displays"] = self._getAttachedDisplaySizesAsStringArray()
		config.conf["brailleViewer"]["autoPositionWindow"] = False

	isDestroyed: bool = False

	def _onClose(self, evt):
		log.debug("braille viewer gui onclose")
		if not evt.CanVeto():
			self.isDestroyed = True
			self.Destroy()
			return
		evt.Veto()

	def _onDestroy(self, evt):
		log.debug("braille viewer gui destroyed")
		self._savePositionInformation()
		self.isDestroyed = True
		self._notifyOfDestroyed()
		evt.Skip()
