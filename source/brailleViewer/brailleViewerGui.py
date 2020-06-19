# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import time
from typing import List

import wx
import gui
import config
from logHandler import log
import fonts
import braille
import inputCore

BRAILLE_UNICODE_PATTERNS_START = 0x2800
BRAILLE_SPACE_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START)
BRAILLE_INIT_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START + 1)
SPACE_CHARACTER = u" "


# Inherit from wx.Frame because these windows show in the alt+tab menu (where miniFrame does not)
# wx.Dialog causes a crash on destruction when multiple were created at the same time (speechViewer
# may start at the same time)
class BrailleViewerFrame(wx.Frame):

	# Translators: The title of the NVDA Braille Viewer tool window.
	_title = _("NVDA Braille Viewer")
	_numCells: int
	_rawTextOutputLastSet: str
	_rawTextOutput: wx.TextCtrl
	_brailleOutputLastSet: str
	_brailleOutput: wx.TextCtrl
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
		self._rawTextOutputLastSet = "".join(f"{x%10}" for x in range(numCells+5))

		self.frameContentsSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SetSizer(self.frameContentsSizer)
		self.panel = wx.Panel(self)
		self.frameContentsSizer.Add(self.panel, proportion=1, flag=wx.EXPAND)

		self.panelContentsSizer = wx.BoxSizer(wx.VERTICAL)
		self.panel.SetSizer(self.panelContentsSizer)

		borderSizer = wx.BoxSizer(wx.VERTICAL)
		self.panelContentsSizer .Add(
			borderSizer,
			proportion=1,
			flag=wx.EXPAND | wx.ALL,
			border=5,
		)
		self._createControls(borderSizer, self.panel)
		self.ShowWithoutActivating()
		self.Fit()

	def _createControls(self, sizer, parent):
		# Translators: The label for the display of the braille cells in the braille viewer.
		self._brailleCellsLabel = _("Braille Cells:")
		# Translators: A label in the braille viewer notifying that cell routing will
		# occur in 'timeRemaining' seconds.
		self._routingToCellLabel = _("Routing to cell under cursor in {timeRemaining}")
		# Hack: use Static text to set the width of the dialog to the number of cells.
		self._brailleIndexesText = self._brailleCellsLabel.ljust(self._numCells + 5, " ")
		self._brailleIndexes = wx.StaticText(parent, label=self._brailleIndexesText)
		self._brailleIndexes.Font = self._setBrailleFont(self._brailleIndexes.GetFont())
		sizer.Add(self._brailleIndexes, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10, proportion=1)

		self._brailleOutput = wx.TextCtrl(parent, value=self._brailleOutputLastSet, style=wx.TE_RICH2)
		self._brailleOutput.Font = self._setBrailleFont(self._brailleOutput.GetFont())
		log.debug(f"Font for braille: {self._brailleOutput.Font.GetNativeFontInfoUserDesc()}")
		sizer.Add(self._brailleOutput, flag=wx.EXPAND, proportion=1)
		self._brailleOutput.Bind(wx.EVT_MOTION, self._mouseMotion)

		self._routeToCellStyle = wx.TextAttr()
		self._brailleOutput.GetStyle(0, self._routeToCellStyle)
		self._normalBGColor = self._brailleOutput.GetBackgroundColour()
		self._routeToCellStyle.SetBackgroundColour(wx.Colour(100, 200, 200))

		self._rawTextOutput = wx.TextCtrl(parent, value=self._rawTextOutputLastSet)
		self._rawTextOutput.Font = self._setRawTextFont(self._rawTextOutput.Font)
		log.debug(f"Font for raw text: {self._rawTextOutput.Font.GetNativeFontInfoUserDesc()}")
		sizer.Add(self._rawTextOutput, flag=wx.EXPAND, proportion=1)

		optionsSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a setting in the braille viewer that controls
		# whether the braille viewer is shown at startup or not.
		showOnStartupCheckboxLabel = _("&Show Braille Viewer on Startup")
		self._shouldShowOnStartupCheckBox = wx.CheckBox(
			parent=parent,
			label=showOnStartupCheckboxLabel)
		self._shouldShowOnStartupCheckBox.SetValue(config.conf["brailleViewer"]["showBrailleViewerAtStartup"])
		self._shouldShowOnStartupCheckBox.Bind(wx.EVT_CHECKBOX, self._onShouldShowOnStartupChanged)
		optionsSizer.Add(self._shouldShowOnStartupCheckBox)

		# Translators: The label for a setting in the braille viewer that controls
		# whether hovering mouse routes to the cell.
		hoverRoutesCellText = _("&Hover to route to cell")
		self._shouldHoverRouteToCellCheckBox = wx.CheckBox(
			parent=parent,
			label=hoverRoutesCellText
		)
		self._shouldHoverRouteToCellCheckBox.SetValue(config.conf["brailleViewer"]["shouldHoverRouteToCell"])
		self._shouldHoverRouteToCellCheckBox.Bind(wx.EVT_CHECKBOX, self._onShouldHoverRouteToCellCheckBoxChanged)
		optionsSizer.Add(self._shouldHoverRouteToCellCheckBox)

		sizer.Add(optionsSizer, flag=wx.EXPAND|wx.TOP, border=5)

	hitResMap = {
		wx.TE_HT_UNKNOWN: "TE_HT_UNKNOWN",  # this means HitTest() is simply not implemented
		wx.TE_HT_BEFORE: "TE_HT_BEFORE",  # either to the left or upper
		wx.TE_HT_ON_TEXT: "TE_HT_ON_TEXT",  # directly on
		wx.TE_HT_BELOW: "TE_HT_BELOW",  # below [the last line]
		wx.TE_HT_BEYOND: "TE_HT_BEYOND",
	}

	_lastMouseOverChar = None
	_mouseOverTime = None
	_secondsBeforeRouting = 3
	driverName = "brailleViewer"
	keyRouting = "route"

	def _setBrailleCellsLabel(self, label):
		self._brailleIndexesText = label
		self._brailleIndexes.Label = label.ljust(self._numCells + 5, " ")

	def _doRouting(self, routeToIndex):
		result2, index2 = self._brailleOutput.HitTestPos(
			self._brailleOutput.ScreenToClient(wx.GetMousePosition())
		)
		if result2 != wx.TE_HT_ON_TEXT or not (index2 == self._lastMouseOverChar == routeToIndex):
			return  # cancel
		timeElapsed = time.time() - self._mouseOverTime
		if timeElapsed < self._secondsBeforeRouting:
			timeRemaining = self._secondsBeforeRouting - int(timeElapsed)
			countdownLabel = self._routingToCellLabel.format(timeRemaining=timeRemaining)
			if self._brailleIndexesText != countdownLabel:
				self._setBrailleCellsLabel(countdownLabel)
			wx.CallLater(50, self._doRouting, routeToIndex)
		else:
			self._setBrailleCellsLabel(self._brailleCellsLabel)
			self._brailleOutput.SetBackgroundColour(self._normalBGColor)
			import globalCommands
			inputCore.manager.executeGesture(
				BrailleViewerInputGesture(self.keyRouting, routeToIndex)
			)

	def _resetBrailleCellsLabel(self):
		self.Freeze()
		self._setBrailleCellsLabel(self._brailleCellsLabel)
		self._brailleOutput.SetBackgroundColour(self._normalBGColor)
		self._lastMouseOverChar = None  # cancels _doRouting
		self.Thaw()
		self.Refresh()
		self.Update()

	def _mouseMotion(self, evt: wx.MouseEvent):
		if not self._shouldHoverRouteToCellCheckBox.Value:
			return
		result, index = self._brailleOutput.HitTestPos(evt.GetPosition())
		if result == wx.TE_HT_ON_TEXT:
			if self._lastMouseOverChar != index:
				lastIndex = self._lastMouseOverChar
				self._lastMouseOverChar = index
				if lastIndex is not None:
					normalText = wx.TextAttr()
					normalText.SetBackgroundColour(self._normalBGColor)
					self._brailleOutput.SetStyle(lastIndex, lastIndex + 1, normalText)
				self._brailleOutput.SetStyle(index, index + 1, self._routeToCellStyle)
				self._mouseOverTime = time.time()
				self._doRouting(index)
		elif self._lastMouseOverChar is not None:
			self._resetBrailleCellsLabel()

	def _onShouldShowOnStartupChanged(self, evt):
		config.conf["brailleViewer"]["showBrailleViewerAtStartup"] = self._shouldShowOnStartupCheckBox.IsChecked()

	def _onShouldHoverRouteToCellCheckBoxChanged(self, evt: wx.CommandEvent):
		config.conf["brailleViewer"]["shouldHoverRouteToCell"] = self._shouldHoverRouteToCellCheckBox.IsChecked()
		if not evt.IsChecked():
			self._resetBrailleCellsLabel()

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

		padToLen = currentCellCount + 2  # Ensure all content is displayed, append 2 extra space characters
		adjustOffsetsToUnicode = u"".join([
			chr(BRAILLE_UNICODE_PATTERNS_START + cell)
			for cell in cells
		])

		# Determine what we must update
		brailleEqual = self._brailleOutputLastSet == adjustOffsetsToUnicode
		textEqual = self._rawTextOutputLastSet == rawText
		if brailleEqual and textEqual:
			# Exit early if we do not have to update either label.
			return

		# Update the GUI
		# Freeze so that we don't see flickering while updates take place.
		self.Freeze()
		if not brailleEqual:
			self._brailleOutputLastSet = adjustOffsetsToUnicode
			# Create a unicode string that is at least as long as expected.
			# A later call to `Fit` will ensure that strings that are too long are handled.
			paddedBraille = adjustOffsetsToUnicode.ljust(padToLen, BRAILLE_SPACE_CHARACTER)
			self._brailleOutput.SetValue(paddedBraille)
			index = self._lastMouseOverChar
			if index is not None:
				self._brailleOutput.SetStyle(index, index + 1, self._routeToCellStyle)
		if not textEqual:
			self._rawTextOutputLastSet = rawText
			paddedRawText = rawText.ljust(padToLen, " ")
			self._rawTextOutput.SetValue(paddedRawText)

		if self._numCells != currentCellCount:
			# do resize
			log.debug(f"Updating brailleViewer cell count to: {currentCellCount}")
			self._numCells = currentCellCount
			self._setBrailleCellsLabel(self._brailleIndexesText)
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

	def saveInfoAndDestroy(self):
		self._savePositionInformation()
		self.isDestroyed = True
		self.Destroy()

	def _onClose(self, evt):
		log.debug("braille viewer gui onclose")
		self.saveInfoAndDestroy()

	def _onDestroy(self, evt):
		log.debug("braille viewer gui onDestroy")
		self.isDestroyed = True
		self._notifyOfDestroyed()
		evt.Skip()


class BrailleViewerInputGesture(braille.BrailleDisplayGesture):

	source = BrailleViewerFrame.driverName

	def __init__(self, command, argument):
		super().__init__()
		self.id = command
		if command == BrailleViewerFrame.keyRouting:
			self.routingIndex = argument
			import globalCommands
			self.script = globalCommands.commands.script_braille_routeTo
