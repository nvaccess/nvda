# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import time
from typing import List, Tuple, Optional

import wx
import gui
import config
from logHandler import log
import fonts
import inputCore

BRAILLE_UNICODE_PATTERNS_START = 0x2800
BRAILLE_SPACE_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START)
BRAILLE_INIT_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START + 1)
SPACE_CHARACTER = u" "
TIMER_INTERVAL = 32


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
		self._secondsOfHoverToActivate = config.conf["brailleViewer"]["secondsOfHoverToActivate"]
		self._lastMouseOverChar = None
		self._mouseOverTime = None
		self._secondsBeforeReturnToNormal = self._secondsOfHoverToActivate + 0.4
		self._doneRouteCall = False
		self._newBraille: Optional[str] = None
		self._newRawText: Optional[str] = None
		self._newSize: Optional[int] = None

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
		self.panel.SetDoubleBuffered(on=True)  # fix for flickering during rapid updates.
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
		self._timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, lambda evt: self._updateGui())
		self._createControls(borderSizer, self.panel)
		self.ShowWithoutActivating()
		self.Fit()

	def _createControls(self, sizer, parent):
		# Hack: use Static text to calculate the width of the dialog required for the number of cells.
		self._brailleSizeTest = wx.StaticText(parent, label=(self._numCells + 5) * " ")
		# Use the same font so the size is accurate.
		self._brailleSizeTest.Font = self._setBrailleFont(self._brailleSizeTest.GetFont())
		# Keep the label hidden since it provides no information.
		self._brailleSizeTest.Hide()
		labelSize = self._brailleSizeTest.GetSize()
		sizer.Add(self._brailleSizeTest, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10, proportion=1)

		self._brailleOutput = wx.TextCtrl(
			parent,
			value=self._brailleOutputLastSet,
			style=wx.TE_RICH | wx.TE_READONLY,
			size=wx.Size(labelSize.x, -1)
		)
		self._brailleOutput.Font = self._setBrailleFont(self._brailleOutput.GetFont())
		log.debug(f"Font for braille: {self._brailleOutput.Font.GetNativeFontInfoUserDesc()}")
		sizer.Add(self._brailleOutput, flag=wx.EXPAND, proportion=1)
		if self._shouldDoHover():
			self._brailleOutput.Bind(wx.EVT_MOTION, self._mouseOver)

		self._normalBGColor = self._brailleOutput.GetBackgroundColour()
		self._hoverCellStyle = self._normalBGColor

		self._rawTextOutput = wx.TextCtrl(
			parent,
			value=self._rawTextOutputLastSet,
			style=wx.TE_RICH2 | wx.TE_READONLY
		)
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
		hoverRoutesCellText = _("&Hover for cell routing")
		self._shouldHoverRouteToCellCheckBox = wx.CheckBox(
			parent=parent,
			label=hoverRoutesCellText
		)
		self._shouldHoverRouteToCellCheckBox.SetValue(self._shouldDoHover())
		self._shouldHoverRouteToCellCheckBox.Bind(wx.EVT_CHECKBOX, self._onShouldHoverRouteToCellCheckBoxChanged)
		optionsSizer.Add(self._shouldHoverRouteToCellCheckBox)
		sizer.Add(optionsSizer, flag=wx.EXPAND|wx.TOP, border=5)

	def _shouldDoHover(self):
		return config.conf["brailleViewer"]["shouldHoverRouteToCell"]

	hitResMap = {
		wx.TE_HT_UNKNOWN: "TE_HT_UNKNOWN",  # this means HitTest() is simply not implemented
		wx.TE_HT_BEFORE: "TE_HT_BEFORE",  # either to the left or upper
		wx.TE_HT_ON_TEXT: "TE_HT_ON_TEXT",  # directly on
		wx.TE_HT_BELOW: "TE_HT_BELOW",  # below [the last line]
		wx.TE_HT_BEYOND: "TE_HT_BEYOND",
	}

	def _mouseOver(self, evt: wx.MouseEvent):
		if (
			self._shouldDoHover()
			# If the timer is already running, updateHover is already being called.
			and not self._timer.IsRunning()
		):
			self._updateHover()

	def _linearInterpolate(self, value, start, end):
		difference = tuple(map(lambda i, j: i - j, end, start))
		return tuple(map(lambda i, j: i + value * j, start, difference))

	def _calculateHoverColour(
			self,
			timeElapsed: float,
			totalTime: float,
			startValue: float,
			startColor: wx.Colour,
			finalColor: wx.Colour
	):
		finalColorT = finalColor.Get(includeAlpha=False)
		value = min(1.0, max(0.0, (0.001 + timeElapsed) / totalTime))
		initialColor: Tuple[int, int, int] = startColor.Get(includeAlpha=False)
		startColor = self._linearInterpolate(startValue, initialColor, finalColorT)
		currentColor = self._linearInterpolate(value, startColor, finalColorT)
		return wx.Colour(*currentColor)

	def _updateHoverCell(self):
		normalStyle = wx.TextAttr()
		normalStyle.SetBackgroundColour(self._normalBGColor)
		index = self._lastMouseOverChar
		length = len(self._brailleOutput.GetValue())
		if index is not None:
			self._brailleOutput.SetStyle(index, index + 1, self._hoverCellStyle)
			self._brailleOutput.SetStyle(0, index, normalStyle)
			self._brailleOutput.SetStyle(index + 1, length, normalStyle)
		else:
			self._brailleOutput.SetStyle(0, length, normalStyle)

	def _updateHoverStyleColor(self, newColor: wx.Colour):
		self._hoverCellStyle = wx.TextAttr()
		self._hoverCellStyle.SetBackgroundColour(newColor)

	def _updateGui(self):
		self.Freeze()
		if self._newBraille is not None:
			self._brailleOutput.SetValue(self._newBraille)
			self._newBraille = None
		if self._newRawText is not None:
			self._rawTextOutput.SetValue(self._newRawText)
			self._newRawText = None
		if self._newSize is not None:
			# do resize
			log.debug(
				f"Updating brailleViewer cell count to: {self._newSize}"
				f", old braille label size: {self._brailleSizeTest.GetSize()}"
			)
			self._numCells = self._newSize
			self._brailleSizeTest.Label = (self._numCells + 5) * " "
			labelSize = self._brailleSizeTest.GetSize()
			log.debug(f"New braille label size {labelSize}")
			self._brailleOutput.SetMinSize(size=wx.Size(labelSize.x, -1))
			# Ensure that any variation in the number of characters displayed is still shown by calling `Fit`.
			# This should really only happen when an external display with a different cell count is connected.
			# If there is some other reason, it is better for the window size to adjust, than to miss content.
			self.Fit()
			self._newSize = None

		if self._debugGuiUpdate:
			self._doDebugGuiUpdate()

		self._updateHover()
		self._updateHoverCell()
		self.Thaw()

	_debugGuiIndex = 0
	_debugGuiUpdate = False

	def _doDebugGuiUpdate(self):
		normalColour = self._rawTextOutput.GetForegroundColour()
		normalStyle = wx.TextAttr(normalColour, colBack=self._normalBGColor)
		self._rawTextOutput.SetStyle(2 + self._debugGuiIndex, 2 + self._debugGuiIndex + 1, normalStyle)

		self._debugGuiIndex = (self._debugGuiIndex + 1) % 4
		activeIndexStyle = wx.TextAttr(normalColour, colBack=wx.Colour(0, 0, 255))
		self._rawTextOutput.SetStyle(2 + self._debugGuiIndex, 2 + self._debugGuiIndex + 1, activeIndexStyle)

		enabledStyle = wx.TextAttr(normalColour, colBack=wx.Colour(0, 255, 0))
		disableStyle = wx.TextAttr(normalColour, colBack=wx.Colour(255, 0, 0))
		if self._timer.IsOneShot():
			self._rawTextOutput.SetStyle(1, 2, enabledStyle)
		else:
			self._rawTextOutput.SetStyle(1, 2, disableStyle)
		if self._timer.IsRunning():
			self._rawTextOutput.SetStyle(0, 1, enabledStyle)
		else:
			self._rawTextOutput.SetStyle(0, 1, disableStyle)

	def _setPreActivateStyle(self, secondsSinceHoverStart):
		self._updateHoverStyleColor(
			self._calculateHoverColour(
				secondsSinceHoverStart,
				self._secondsOfHoverToActivate,
				startValue=0.2,
				startColor=self._normalBGColor,
				finalColor=wx.Colour(255, 205, 60)  # orange-yellow
			))

	def _setPostActivateStyle(self, secondsSinceHoverStart):
		self._updateHoverStyleColor(self._calculateHoverColour(
			secondsSinceHoverStart - self._secondsOfHoverToActivate,
			totalTime=self._secondsBeforeReturnToNormal - self._secondsOfHoverToActivate,
			startValue=0.0,
			startColor=wx.Colour(81, 215, 81),  # green
			finalColor=self._normalBGColor
		))

	def _cancelPendingHover(self):
		self._lastMouseOverChar = None  # cancels a pending hover action
		self._doneRouteCall = False
		self._mouseOverTime = time.time()
		self._updateHoverStyleColor(self._normalBGColor)

	def _startPendingHover(self, index):
		self._cancelPendingHover()
		self._lastMouseOverChar = index

	def _getBrailleIndexUnderMouse(self) -> Optional[int]:
		mousePos = wx.GetMousePosition()
		toClient = self._brailleOutput.ScreenToClient(mousePos)
		# This hit test is inaccurate, there seems to be a bug in wx.
		# When the mouse is above or before the window it is counted as a hit.
		# Above: mouseY is less than windowY I.E. when 'toClient.y' < 0
		# Before: mouseX is less than winsowX I.E. when 'toClient.x' < 0
		result, index = self._brailleOutput.HitTestPos(
			toClient
		)
		if result == wx.TE_HT_ON_TEXT and toClient.y > 0 and toClient.x > 0:
			return index
		return None

	def _updateHover(self):
		if not self._shouldDoHover():
			return
		index = self._getBrailleIndexUnderMouse()
		if index is None:
			# Mouse no longer over braille cells
			self._cancelPendingHover()
			self._timer.Stop()
			self._timer.StartOnce()
			return
		elif not self._timer.IsRunning() or self._timer.IsOneShot():
			self._timer.Start(milliseconds=TIMER_INTERVAL)
		if index != self._lastMouseOverChar:
			# Mouse over a new braille cell, start hover process again.
			self._startPendingHover(index)
		self._updateHoverStage()

	def _activateRouteToCell(self):
		from .brailleViewerInputGesture import BrailleViewerGesture_RouteTo
		inputCore.manager.executeGesture(
			BrailleViewerGesture_RouteTo(self._lastMouseOverChar)
		)

	def _updateHoverStage(self):
		""" Update visualization of hover, over time.
		"""
		timeElapsed = time.time() - self._mouseOverTime
		if timeElapsed < self._secondsOfHoverToActivate:
			self._setPreActivateStyle(timeElapsed)
		elif timeElapsed < self._secondsBeforeReturnToNormal:
			self._setPostActivateStyle(timeElapsed)
			if not self._doneRouteCall:  # ensure activation only happens once.
				self._activateRouteToCell()
				self._doneRouteCall = True
		else:
			# This hover is now complete, don't reset _lastMouseOverChar, the hover shouldn't start again.
			self._updateHoverStyleColor(self._normalBGColor)

	def _onShouldShowOnStartupChanged(self, evt):
		config.conf["brailleViewer"]["showBrailleViewerAtStartup"] = self._shouldShowOnStartupCheckBox.IsChecked()

	def _onShouldHoverRouteToCellCheckBoxChanged(self, evt: wx.CommandEvent):
		config.conf["brailleViewer"]["shouldHoverRouteToCell"] = evt.IsChecked()
		if not evt.IsChecked():
			self._brailleOutput.Unbind(wx.EVT_MOTION, source=None, handler=self._mouseOver)
			self._cancelPendingHover()
			self._timer.Stop()
			self._timer.StartOnce()
		else:
			self._brailleOutput.Bind(wx.EVT_MOTION, handler=self._mouseOver)

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
		if not brailleEqual:
			self._brailleOutputLastSet = adjustOffsetsToUnicode
			# Create a unicode string that is at least as long as expected.
			# A later call to `Fit` will ensure that strings that are too long are handled.
			paddedBraille = adjustOffsetsToUnicode.ljust(padToLen, BRAILLE_SPACE_CHARACTER)
			self._newBraille = paddedBraille
		if not textEqual:
			self._rawTextOutputLastSet = rawText
			paddedRawText = rawText.ljust(padToLen, " ")
			self._newRawText = paddedRawText
		if self._numCells != currentCellCount:
			self._newSize = currentCellCount
		if not self._timer.IsRunning():
			self._timer.StartOnce()

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

