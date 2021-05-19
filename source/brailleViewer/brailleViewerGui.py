# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2021 NV Access Limited, Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import enum
import time
from typing import List, Optional

import wx
import gui
import config
from logHandler import log
import fonts
import inputCore
import gui.contextHelp

BRAILLE_UNICODE_PATTERNS_START = 0x2800
BRAILLE_SPACE_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START)
BRAILLE_INIT_CHARACTER = chr(BRAILLE_UNICODE_PATTERNS_START + 1)
SPACE_CHARACTER = u" "
TIMER_INTERVAL = 32


def _linearInterpolate(value, start, end):
	difference = tuple(map(lambda i, j: i - j, end, start))
	return tuple(map(lambda i, j: i + value * j, start, difference))


def _getCharIndexUnderMouse(ctrl: wx.TextCtrl) -> Optional[int]:
	""" Get the index of the character under the mouse.
	@note: Assumes all characters are on one line
	"""
	mousePos = wx.GetMousePosition()
	toClient = ctrl.ScreenToClient(mousePos)
	# This hit test is inaccurate, there seems to be a bug in wx.
	# When the mouse is above or before the window it is counted as a hit.
	# Above: mouseY is less than windowY I.E. when 'toClient.y' < 0
	# Before: mouseX is less than windowX I.E. when 'toClient.x' < 0
	result, index = ctrl.HitTestPos(
		toClient
	)
	if result == wx.TE_HT_ON_TEXT and toClient.y > 0 and toClient.x > 0:
		return index
	return None


def _shouldDoHover():
	return config.conf["brailleViewer"]["shouldHoverRouteToCell"]


def createBackgroundColorTextAttr(newColor: wx.Colour) -> wx.TextAttr:
	attr = wx.TextAttr()
	attr.SetBackgroundColour(newColor)
	return attr


class CharCellBackgroundColorAnimation:
	""" Transition from one colour to another over time for a character cell background.
	"""
	def __init__(
			self,
			textCtrl: wx.TextCtrl,
			textCellIndex: int,
			startValue: float,
			originColor: wx.Colour,
			destColor: wx.Colour,
			durationSeconds: float,
	):
		"""
		:param textCtrl: the TextCtrl to perform the background colour animation on.
		:param textCellIndex: the character cell index that should be highlighted with the animation
		:param startValue: a percentage (0->1). At elapsed == 0 the colour transition will already be
			this far through. Allows for a beginning bump in the colour transition.
		:param originColor: The origin colour.
		:param destColor: The destination colour. Reached at elapsed == totalTime.
		:param durationSeconds: total time that the transition should take in seconds
		"""
		self._textCtrl = textCtrl
		self._textCellIndex = textCellIndex
		self._originColor = originColor
		self._destColor = destColor
		self._startValue = startValue
		self._durationSeconds = durationSeconds
		self._startTime = time.time()
		normalBGColor = textCtrl.GetBackgroundColour()
		self._currentAttr = self._normalBGStyle = createBackgroundColorTextAttr(normalBGColor)

	def update(self):
		accumulatedElapsedTime = time.time() - self._startTime
		# [0..1] proportion accumulatedElapsedTime is through totalTime
		normalisedElapsed = min(1.0, max(0.0, (0.001 + accumulatedElapsedTime) / self._durationSeconds))
		colourTransitionValue = self._startValue + normalisedElapsed * (1 - self._startValue)
		currentColorTuple = _linearInterpolate(
			colourTransitionValue,
			self._originColor.Get(includeAlpha=False),
			self._destColor.Get(includeAlpha=False)
		)
		currentStyle = createBackgroundColorTextAttr(wx.Colour(*currentColorTuple))
		index = self._textCellIndex
		length = len(self._textCtrl.GetValue())
		self._textCtrl.SetStyle(index, index + 1, currentStyle)
		self._textCtrl.SetStyle(0, index, self._normalBGStyle)
		self._textCtrl.SetStyle(index + 1, length, self._normalBGStyle)

	def resetColor(self):
		length = len(self._textCtrl.GetValue())
		self._textCtrl.SetStyle(0, length, self._normalBGStyle)


class TextCellHover:
	"""Tracks a the mouse hovering over a cell in a textCtrl.
	"""

	@enum.unique
	class Stage(enum.Enum):
		NOT_STARTED = enum.auto()
		HOVER_PENDING = enum.auto()
		ACTIVATED = enum.auto()
		FINISHED = enum.auto()
		CANCELLED = enum.auto()

	def __init__(self, textCtrl: wx.TextCtrl):
		self._secondsOfHoverToActivate = config.conf["brailleViewer"]["secondsOfHoverToActivate"]
		self._secondsOfPostActivate = 0.4
		self._textCtrl = textCtrl
		self._normalBGColor = textCtrl.GetBackgroundColour()
		self._charIndex = None
		self._doneRouteCall = False
		self._cellAnimation: Optional[CharCellBackgroundColorAnimation] = None
		self._setStage(self.Stage.NOT_STARTED)

	def isInProgress(self) -> bool:
		return self._stage not in [
			self.Stage.NOT_STARTED,
			self.Stage.FINISHED,
			# Cancelled still requires a state change.
		]

	def _setStage(self, newStage: Stage):
		self._stage = newStage
		self._stageStartTime = time.time()

	def cancelPendingHover(self):
		self._charIndex: Optional[int] = None  # cancels a pending hover action
		self._setStage(self.Stage.CANCELLED)

	def startPendingHover(self, index):
		self._charIndex = index
		self._setStage(self.Stage.HOVER_PENDING)
		# set pre-activate style
		self._cellAnimation = CharCellBackgroundColorAnimation(
			self._textCtrl,
			index,
			startValue=0.2,
			originColor=self._normalBGColor,
			destColor=wx.Colour(255, 205, 60),  # orange-yellow
			durationSeconds=self._secondsOfHoverToActivate
		)

	def _setPostActivateStyle(self):
		self._cellAnimation = CharCellBackgroundColorAnimation(
			self._textCtrl,
			self._charIndex,
			startValue=0.0,
			originColor=wx.Colour(81, 215, 81),  # green
			destColor=self._normalBGColor,
			durationSeconds=self._secondsOfPostActivate
		)

	def doHoverTracking(self):
		if not _shouldDoHover():
			return
		index = _getCharIndexUnderMouse(self._textCtrl)

		if index == self._charIndex:
			return
		if index is None:
			# Mouse no longer over braille cells
			self.cancelPendingHover()
			return
		# Mouse over a new braille cell, start hover process again.
		self.startPendingHover(index)

	def updateControls(self):
		self._updateHoverStage()
		if self._cellAnimation:
			self._cellAnimation.update()

	def _updateHoverStage(self):
		""" Update visualization of hover, over time.
		"""
		if not self.isInProgress():
			return
		timeElapsed = time.time() - self._stageStartTime
		if (
			self._stage == self.Stage.HOVER_PENDING
			and timeElapsed > self._secondsOfHoverToActivate
		):
			self._activateRouteToCell()
			self._setPostActivateStyle()
			self._setStage(self.Stage.ACTIVATED)
		elif (
			self._stage == self.Stage.ACTIVATED
			and timeElapsed > self._secondsOfPostActivate
		):
			# This hover is now complete, don't reset _charIndex, the hover shouldn't start again.
			self._setStage(self.Stage.FINISHED)
			self._cellAnimation.resetColor()
			self._cellAnimation = None
		elif self._stage == self.Stage.CANCELLED:
			self._setStage(self.Stage.NOT_STARTED)
			if self._cellAnimation:
				self._cellAnimation.resetColor()
				self._cellAnimation = None

	def _activateRouteToCell(self):
		from .brailleViewerInputGesture import BrailleViewerGesture_RouteTo
		inputCore.manager.executeGesture(
			BrailleViewerGesture_RouteTo(self._charIndex)
		)


def _setBrailleFont(fontName: str, textCtrl: wx.Control) -> wx.Font:
	fonts.importFonts()
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
	font: wx.Font = textCtrl.GetFont()
	font.SetPointSize(20)
	font.SetFaceName(fontName)
	textCtrl.SetFont(font)
	return font


# Inherit from wx.Frame because these windows show in the alt+tab menu (where miniFrame does not)
# wx.Dialog causes a crash on destruction when multiple were created at the same time (speechViewer
# may start at the same time)
class BrailleViewerFrame(
		gui.contextHelp.ContextHelpMixin,
		wx.Frame  # wxPython does not seem to call base class initializer, put last in MRO
):

	helpId = "BrailleViewer"

	# Translators: The title of the NVDA Braille Viewer tool window.
	_title = _("NVDA Braille Viewer")
	_numCells: int
	_rawTextOutputLastSet: str
	_rawTextOutput: wx.TextCtrl
	_brailleOutputLastSet: str
	_brailleOutput: wx.TextCtrl
	_shouldShowOnStartupCheckBox: wx.CheckBox
	#: True if _mouseOver has been bound to mouse moved events.
	_mouseMotionBound: bool = False

	def __init__(self, numCells, onDestroyed):
		log.debug(f"Starting braille viewer with {numCells} cells")

		dialogPos = wx.DefaultPosition
		if not config.conf["brailleViewer"]["autoPositionWindow"] and self._doDisplaysMatchConfig():
			log.debug("Setting brailleViewer window position")
			brailleViewSection = config.conf["brailleViewer"]
			dialogPos = wx.Point(x=brailleViewSection["x"], y=brailleViewSection["y"])
		self._newBraille: Optional[str] = None
		self._newRawText: Optional[str] = None
		self._newCellCount: Optional[int] = None

		super().__init__(
			gui.mainFrame,
			title=self._title,
			pos=dialogPos,
			style=wx.CAPTION | wx.CLOSE_BOX | wx.STAY_ON_TOP
		)
		self.Bind(wx.EVT_CLOSE, self._onClose)
		self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy)

		self._notifyOfDestroyed = onDestroyed
		self._numCells = numCells
		self._brailleOutputLastSet = BRAILLE_SPACE_CHARACTER * numCells
		self._rawTextOutputLastSet = ""

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

		# The timer ensures that updates and animations happen smoothly.
		# When hover to route is enabled (and the mouse is over the window) the timer is running to regularly
		# call _updateGui. When the mouse leaves the window, or if hover to route is disabled, the timer is
		# used as a "one-shot" timer only when there are update to what should be displayed.
		self._timer: wx.Timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, lambda evt: self._updateGui())

		self._createControls(borderSizer, self.panel)
		self.ShowWithoutActivating()
		self.Fit()

	def _createBrailleTextSizeTestCtrl(self, sizer, parent):
		self._brailleSizeTest = wx.StaticText(parent)
		# Use the same font so the size is accurate.
		_setBrailleFont(
			"FreeMono-FixedBraille",
			self._brailleSizeTest
		)

		# Keep the label hidden since it provides no information.
		# Don't destroy it, it will be used later if
		# the number of cells changes (if another braille display is connected with a different cell count)
		self._brailleSizeTest.Hide()
		sizer.Add(self._brailleSizeTest, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10, proportion=1)

	def _calculateBrailleOutputSize(self, numCells: int) -> wx.Size:
		self._brailleSizeTest.SetLabel((numCells + 5) * " ")
		return self._brailleSizeTest.GetSize()

	def _createControls(self, sizer, parent):
		# There seems to be no way to make a TextCtrl (used for braille and raw text output) match its
		# text content: https://forums.wxwidgets.org/viewtopic.php?t=44472
		# Hacky fix:
		# Use a Static text to calculate the width of the dialog required for the number of cells.
		self._createBrailleTextSizeTestCtrl(sizer, parent)
		labelSize = self._calculateBrailleOutputSize(self._numCells)
		log.debug(f"Initial braille label size {labelSize}")

		self._brailleOutput = wx.TextCtrl(
			parent,
			value=self._brailleOutputLastSet,
			style=wx.TE_RICH | wx.TE_READONLY,
			size=wx.Size(labelSize.x, -1)
		)
		_setBrailleFont(
			"FreeMono-FixedBraille",
			self._brailleOutput
		)
		log.debug(f"Font for braille: {self._brailleOutput.GetFont().GetNativeFontInfoUserDesc()}")
		sizer.Add(self._brailleOutput, flag=wx.EXPAND, proportion=1)

		self._hoverTracker = TextCellHover(self._brailleOutput)

		self._rawTextOutput = wx.TextCtrl(
			parent,
			value=self._rawTextOutputLastSet,
			style=wx.TE_RICH2 | wx.TE_READONLY
		)
		_setBrailleFont(
			"FreeMono-FixedBraille",
			self._rawTextOutput
		)
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
		self._shouldHoverRouteToCellCheckBox.Bind(wx.EVT_CHECKBOX, self._onShouldHoverRouteToCellCheckBoxChanged)
		self._shouldHoverRouteToCellCheckBox.SetValue(_shouldDoHover())
		self._updateMouseOverBinding(_shouldDoHover())
		optionsSizer.Add(self._shouldHoverRouteToCellCheckBox)
		sizer.Add(optionsSizer, flag=wx.EXPAND | wx.TOP, border=5)

	def _onShouldShowOnStartupChanged(self, evt):
		config.conf["brailleViewer"]["showBrailleViewerAtStartup"] = self._shouldShowOnStartupCheckBox.IsChecked()

	def _onShouldHoverRouteToCellCheckBoxChanged(self, evt: wx.CommandEvent):
		config.conf["brailleViewer"]["shouldHoverRouteToCell"] = evt.IsChecked()
		self._updateMouseOverBinding(evt.IsChecked())

	def _updateMouseOverBinding(self, shouldReceiveMouseMotion: bool):
		if not shouldReceiveMouseMotion and self._mouseMotionBound:
			self._brailleOutput.Unbind(wx.EVT_MOTION, source=None, handler=self._mouseOver)
			self._mouseMotionBound = False
			self._hoverTracker.cancelPendingHover()
		else:
			self._brailleOutput.Bind(wx.EVT_MOTION, handler=self._mouseOver)
			self._mouseMotionBound = True

	def _mouseOver(self, unused: wx.MouseEvent):
		if _shouldDoHover():
			self._triggerGuiUpdate()

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
			self._newCellCount = currentCellCount

		self._triggerGuiUpdate()

	def _triggerGuiUpdate(self):
		continuousTimerRunning = self._timer.IsRunning() and not self._timer.IsOneShot()
		hoverInProgress = self._hoverTracker.isInProgress()
		if hoverInProgress and not continuousTimerRunning:
			self._timer.Stop()
			self._timer.Start(milliseconds=TIMER_INTERVAL)
		elif not hoverInProgress and not self._timer.IsRunning():
			self._timer.StartOnce()

	def _updateGui(self):
		"""Ensure all GUI updates happen in one place to create a smooth update, all changes should happen
		between freeze and thaw.
		"""
		self.Freeze()
		if self._newBraille is not None:
			self._brailleOutput.SetValue(self._newBraille)
			self._newBraille = None
		if self._newRawText is not None:
			self._rawTextOutput.SetValue(self._newRawText)
			self._newRawText = None
		if self._newCellCount is not None:
			# do resize
			self._numCells = self._newCellCount
			oldSize = self._brailleOutput.GetSize()
			labelSize = self._calculateBrailleOutputSize(self._numCells)
			self._brailleOutput.SetMinSize(size=wx.Size(labelSize.x, -1))
			newSize = self._brailleOutput.GetSize()
			log.debug(
				f"Updating brailleViewer cell count to: {self._newCellCount}"
				f", braille label size {oldSize} -> {newSize}"
			)
			# Ensure that any variation in the number of characters displayed is still shown by calling `Fit`.
			# This should really only happen when an external display with a different cell count is connected.
			# If there is some other reason, it is better for the window size to adjust, than to miss content.
			self.Fit()
			self._newCellCount = None

		self._hoverTracker.doHoverTracking()
		self._hoverTracker.updateControls()
		self.Thaw()
		if not self._hoverTracker.isInProgress():
			self._timer.Stop()

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
		log.debug("braille viewer gui onClose")
		self.saveInfoAndDestroy()

	def _onDestroy(self, evt):
		log.debug("braille viewer gui onDestroy")
		self.isDestroyed = True
		self._notifyOfDestroyed()
		evt.Skip()
