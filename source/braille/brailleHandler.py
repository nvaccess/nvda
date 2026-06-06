# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import contextlib
import ctypes.wintypes
import itertools
import threading
import time
import typing
from typing import (
	TYPE_CHECKING,
	List,
	Optional,
	Set,
	Type,
	Union,
)

import api
import baseObject
import bdDetect
import brailleTables
import brailleViewer
import config
import controlTypes
import easeOfAccess
import extensionPoints
import gui
import hwIo
import inputCore
import keyboardHandler
import louisHelper
import queueHandler
import winBindings.kernel32
import winKernel
import wx
from config.configFlags import (
	BrailleMode,
	ShowMessages,
	TetherTo,
)
from gui.guiHelper import wxCallOnMain
from logHandler import log
from utils.security import objectBelowLockScreenAndWindowsIsLocked, post_sessionLockStateChanged
from winAPI.secureDesktop import post_secureDesktopStateChange

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject
	from speech.types import SpeechSequence


from .buffers import (
	BrailleBuffer,
)
from .constants import (
	AUTO_DISPLAY_NAME,
	CONTEXTPRES_CHANGEDCONTEXT,
	NO_BRAILLE_DISPLAY_NAME,
	TEXT_SEPARATOR,
)
from .display import (
	RENAMED_DRIVERS,
	BrailleDisplayDriver,
	DisplayDimensions,
	_getDisplayDriver,
)
from .extensions import (
	_decide_disabledIncludesMessages,
	_post_dismissBrailleMessage,
	_pre_showBrailleMessage,
	decide_enabled,
	displayChanged,
	displaySizeChanged,
	filter_displayDimensions,
	filter_displaySize,
	pre_writeCells,
)
from .regions.base import TextRegion
from .regions.NVDAObject import NVDAObjectRegion
from .regions.textInfo import TextInfoRegion
from .regions.focus import getFocusContextRegions, getFocusRegions

FALLBACK_TABLE = config.conf.getConfigValidation(("braille", "translationTable")).default
"""Table to use if the output table configuration is invalid."""


def formatCellsForLog(cells: List[int]) -> str:
	"""Formats a sequence of braille cells so that it is suitable for logging.
	The output contains the dot numbers for each cell, with each cell separated by a space.
	A C{-} indicates an empty cell.
	@param cells: The cells to format.
	@return: The formatted cells.
	"""
	# optimisation: This gets called a lot, so needs to be as efficient as possible.
	# List comprehensions without function calls are faster than loops.
	# For str.join, list comprehensions are faster than generator comprehensions.
	return TEXT_SEPARATOR.join(
		["".join([str(dot + 1) for dot in range(8) if cell & (1 << dot)]) if cell else "-" for cell in cells],
	)


class BrailleHandler(baseObject.AutoPropertyObject):
	# TETHER_AUTO, TETHER_FOCUS, TETHER_REVIEW and tetherValues
	# are deprecated, but remain to retain API backwards compatibility
	TETHER_AUTO = TetherTo.AUTO.value
	TETHER_FOCUS = TetherTo.FOCUS.value
	TETHER_REVIEW = TetherTo.REVIEW.value
	tetherValues = [(v.value, v.displayString) for v in TetherTo]

	queuedWrite: Optional[List[int]] = None
	queuedWriteLock: threading.Lock
	ackTimerHandle: int
	_regionsPendingUpdate: Set[Union[NVDAObjectRegion, TextInfoRegion]]
	"""
	Regions pending an update.
	Regions are added by L{handleUpdate} and L{handleCaretMove} and cleared in L{_handlePendingUpdate}.
	"""

	def __init__(self):
		louisHelper.initialize()
		self._table: brailleTables.BrailleTable = brailleTables.getTable(FALLBACK_TABLE)
		self.display: Optional[BrailleDisplayDriver] = None
		self._displayDimensions: DisplayDimensions = DisplayDimensions(1, 0)
		"""
		Internal cache for the displayDimensions property.
		This attribute is used to compare the displaySize output by l{filter_displayDimensions} or l{filter_displaySize}
		with its previous output.
		If the value differs, L{displaySizeChanged} is notified.
		"""
		self._enabled: bool = False
		"""
		Internal cache for the enabled property.
		This attribute is used to compare the enabled output by l{decide_enabled}
		with its previous output.
		If L{decide_enabled} decides to disable the handler, pending output should be cleared.
		"""
		self._regionsPendingUpdate = set()

		self.mainBuffer = BrailleBuffer(self)
		self.messageBuffer = BrailleBuffer(self)
		self._messageCallLater = None
		self.buffer = self.mainBuffer
		self._keyCountForLastMessage = 0
		self._cursorPos = None
		self._cursorBlinkUp = True
		self._cells = []
		self._cursorBlinkTimer = None
		self._autoScrollCallLater: wx.CallLater | None = None
		config.post_configProfileSwitch.register(self.handlePostConfigProfileSwitch)
		if config.conf["braille"]["tetherTo"] == TetherTo.AUTO.value:
			self._tether = TetherTo.FOCUS.value
		else:
			self._tether = config.conf["braille"]["tetherTo"]
		self._detector = None
		self._rawText = ""

		self.queuedWriteLock = threading.Lock()
		self.ackTimerHandle = winKernel.createWaitableTimer()

		post_sessionLockStateChanged.register(self._onSessionLockStateChanged)
		post_secureDesktopStateChange.register(self._onSecureDesktopStateChanged)
		brailleViewer.postBrailleViewerToolToggledAction.register(self._onBrailleViewerChangedState)
		# noqa: F401 avoid module level import to prevent cyclical dependency
		# between speech and braille
		from speech.extensions import pre_speech, pre_speechCanceled

		pre_speech.register(self._showSpeechInBraille)
		pre_speechCanceled.register(self.clearBrailleRegions)

	def terminate(self):
		# noqa: F401 avoid module level import to prevent cyclical dependency
		# between speech and braille
		from speech.extensions import pre_speech, pre_speechCanceled

		pre_speechCanceled.unregister(self.clearBrailleRegions)
		pre_speech.unregister(self._showSpeechInBraille)
		self._disableDetection()
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		self.autoScroll(enable=False)
		config.post_configProfileSwitch.unregister(self.handlePostConfigProfileSwitch)
		post_secureDesktopStateChange.unregister(self._onSecureDesktopStateChanged)
		post_sessionLockStateChanged.unregister(self._onSessionLockStateChanged)
		if self.display:
			self.display.terminate()
			self.display = None
		if self.ackTimerHandle:
			if not winBindings.kernel32.CancelWaitableTimer(self.ackTimerHandle):
				raise ctypes.WinError()
			winKernel.closeHandle(self.ackTimerHandle)
			self.ackTimerHandle = None
		louisHelper.terminate()

	def _clearAll(self) -> None:
		"""Clear the braille buffers and update the braille display."""
		self.autoScroll(enable=False)
		self.mainBuffer.clear()
		if self.buffer is self.messageBuffer:
			self._dismissMessage(False)
		self.update()

	def _onSecureDesktopStateChanged(self, isSecureDesktop: bool):
		self.autoScroll(enable=False)
		self.mainBuffer.clear()
		if not easeOfAccess.isRegistered():
			if isSecureDesktop:
				log.warning("Not disabling braille because not registered in ease of access")
			return
		if isSecureDesktop:
			self._disableDetection()  # Does nothing when detection inactive
			if self.display:
				# Suppress setting the display with empty cells when terminating it.
				self.display._suppressDisplayClear = True
			self.setDisplayByName(NO_BRAILLE_DISPLAY_NAME, isFallback=True)
		else:
			configured = config.conf["braille"]["display"]
			if configured == AUTO_DISPLAY_NAME:
				lastRequested = (self._lastRequestedDisplayName, self._lastRequestedDeviceMatch)
				preferredDevice: bdDetect.DriverAndDeviceMatch | None = (
					lastRequested if all(lastRequested) else None
				)
				self._enableDetection(preferredDevice=preferredDevice)
			else:
				# Note, this is executed on the main thread and can take some time for slower drivers.
				self.setDisplayByName(
					configured,
					isFallback=True,  # Don't write to config
				)

	def _onSessionLockStateChanged(self, isNowLocked: bool):
		"""Clear the braille buffers and update the braille display to prevent leaking potentially sensitive information from a locked session.

		:param isNowLocked: True if the session is now locked; false if it is now unlocked.
		"""
		if isNowLocked:
			self._clearAll()

	table: brailleTables.BrailleTable
	"""Type definition for auto prop '_get_table/_set_table'"""

	def _get_table(self) -> brailleTables.BrailleTable:
		"""The translation table to use for braille output."""
		return self._table

	def _set_table(self, table: brailleTables.BrailleTable):
		self._table = table
		config.conf["braille"]["translationTable"] = table.fileName

	# The list containing the regions that will be shown in braille when the speak function is called
	# and the braille mode is set to speech output
	_showSpeechInBrailleRegions: list[TextRegion] = []

	def _showSpeechInBraille(self, speechSequence: "SpeechSequence"):
		if config.conf["braille"]["mode"] == BrailleMode.FOLLOW_CURSORS.value or not self.enabled:
			return
		_showSpeechInBrailleRegions = self._showSpeechInBrailleRegions
		regionsText = "".join([i.rawText for i in _showSpeechInBrailleRegions])
		if len(regionsText) > 100000:
			return
		text = " ".join([x for x in speechSequence if isinstance(x, str)])
		currentRegions = False
		if _showSpeechInBrailleRegions:
			text = f" {text}"
			currentRegions = True

		region = TextRegion(text)
		region.update()
		_showSpeechInBrailleRegions.append(region)
		self.mainBuffer.regions = _showSpeechInBrailleRegions.copy()
		if not currentRegions:
			self.mainBuffer.focus(_showSpeechInBrailleRegions[0])
		self.mainBuffer.update()
		self.update()

	_suppressClearBrailleRegions: bool = False

	@contextlib.contextmanager
	def suppressClearBrailleRegions(self, script: inputCore.ScriptT):
		from globalCommands import commands

		suppress = script in [commands.script_braille_scrollBack, commands.script_braille_scrollForward]
		self._suppressClearBrailleRegions = suppress
		yield

	def clearBrailleRegions(self):
		if not self._suppressClearBrailleRegions:
			self._showSpeechInBrailleRegions.clear()
		self._suppressClearBrailleRegions = False

	def getTether(self):
		return self._tether

	def setTether(self, tether, auto=False):
		if auto and not self.shouldAutoTether:
			return
		if not auto:
			config.conf["braille"]["tetherTo"] = tether
		if tether == self._tether:
			return
		self._tether = tether
		self.mainBuffer.clear()

	def _get_shouldAutoTether(self) -> bool:
		return self.enabled and config.conf["braille"]["tetherTo"] == TetherTo.AUTO.value

	displaySize: int
	_cache_displaySize = True

	def _get_displaySize(self) -> int:
		"""Returns the display size to use for braille output.
		This is calculated from l{displayDimensions}.
		Handlers can register themselves to L{filter_displayDimensions} to change this value on the fly.
		Therefore, this is a read only property and can't be set.
		"""
		displaySize = self.displayDimensions.displaySize
		# For backwards compatibility, we still set the internal cache.
		self._displaySize = displaySize
		return displaySize

	def _set_displaySize(self, value):
		"""While the display size can be changed while a display is connected
		(for instance see L{brailleDisplayDrivers.alva.BrailleDisplayDriver} split point feature),
		it is not possible to override the display size using this property.
		Consider registering a handler to L{filter_displayDimensions} instead.
		"""
		raise AttributeError(
			f"Can't set displaySize to {value}, consider registering a handler to filter_displayDimensions",
		)

	displayDimensions: DisplayDimensions
	_cache_displayDimensions = True

	def _get_displayDimensions(self) -> DisplayDimensions:
		if not self.display:
			numRows = numCols = 0
		else:
			numRows = self.display.numRows
			numCols = self.display.numCols if numRows > 1 else self.display.numCells
		rawDisplayDimensions = DisplayDimensions(
			numRows=numRows,
			numCols=numCols,
		)
		filteredDisplayDimensions = filter_displayDimensions.apply(rawDisplayDimensions)
		# Would be nice if there were a more official way to find out if the displaySize filter is currently registered by at least 1 handler.
		calculatedDisplaySize = filteredDisplayDimensions.displaySize
		if next(filter_displaySize.handlers, None):
			# There is technically a race condition here if a handler is unregistered before the apply call.
			# But worse case is that a multiline display will be singleline for a short time.
			filteredDisplaySize = filter_displaySize.apply(calculatedDisplaySize)
			if filteredDisplaySize != calculatedDisplaySize:
				calculatedDisplaySize = filteredDisplaySize
				filteredDisplayDimensions = DisplayDimensions(
					numRows=1,
					numCols=filteredDisplaySize,
				)
		if self._displayDimensions != filteredDisplayDimensions:
			displaySizeChanged.notify(
				displaySize=calculatedDisplaySize,
				numRows=filteredDisplayDimensions.numRows,
				numCols=filteredDisplayDimensions.numCols,
			)
		self._displayDimensions = filteredDisplayDimensions
		return filteredDisplayDimensions

	def _set_displayDimensions(self, value: DisplayDimensions):
		"""
		It is not possible to override the display dimensions using this property.
		Consider registering a handler to L{filter_displayDimensions} instead.
		"""
		raise AttributeError(
			f"Can't set displayDimensions to {value}, consider registering a handler to filter_displayDimensions",
		)

	enabled: bool
	_cache_enabled = True

	def _get_enabled(self):
		"""Returns whether braille is enabled.
		Handlers can register themselves to L{decide_enabled} and return C{False}
		to forcefully disable the braille handler.
		If components need to change the state from disabled to enabled instead,
		they should register to L{filter_displaySize}.
		By default, the enabled/disabled state is based on the boolean value of L{displaySize},
		and thus is C{True} when the display size is greater than 0.
		This is a read only property and can't be set.
		"""
		self._refreshEnabled()
		return self._enabled

	def _refreshEnabled(self, *, block: bool = False) -> None:
		"""Refresh the state of the enabled property.

		If it has gone from ``True`` to ``False``,
		actions such as dismissing the current message (if any),
		and clearing the cursor blink interval are performed.
		These actions are performed synchronously or asynchronously depending on the value of :param:`block`.

		:param block: Whether this operation should be blocking, defaults to False
		"""
		currentEnabled = bool(self.displaySize) and decide_enabled.decide()
		if self._enabled != currentEnabled:
			self._enabled = currentEnabled
			if currentEnabled is False:
				if block:
					wxCallOnMain(self._handleEnabledDecisionFalse)
				else:
					wx.CallAfter(self._handleEnabledDecisionFalse)

	def _set_enabled(self, value):
		raise AttributeError(
			f"Can't set enabled to {value}, consider registering a handler to decide_enabled or filter_displaySize",
		)

	def _handleEnabledDecisionFalse(self):
		"""When a decider handler decides to disable the braille handler, ensure braille doesn't continue.
		This should be called from the main thread to avoid wx assertions.
		"""
		if self._cursorBlinkTimer:
			# A blinking cursor should be stopped
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		if self.buffer is self.messageBuffer:
			self._dismissMessage(shouldUpdate=False)

	_lastRequestedDisplayName: str | None = None
	"""The name of the last requested braille display driver with setDisplayByName,
	even if it failed and has fallen back to no braille.
	"""
	_lastRequestedDeviceMatch: bdDetect.DeviceMatch | None = None
	"""The last requested device match belonging to _lastRequestedDisplayName,
	even if it failed and has fallen back to no braille.
	"""

	def setDisplayByName(
		self,
		name: str,
		isFallback: bool = False,
		detected: typing.Optional[bdDetect.DeviceMatch] = None,
	) -> bool:
		if name == AUTO_DISPLAY_NAME:
			# Calling _enableDetection will set the display to noBraille until a display is detected.
			# Note that L{isFallback} is ignored in these cases.
			self._enableDetection()
			return True
		elif not isFallback:
			# #8032: Take note of the display requested, even if it is going to fail.
			self._lastRequestedDisplayName = name
			self._lastRequestedDeviceMatch = detected
			if not detected:
				self._disableDetection()

		try:
			newDisplayClass = _getDisplayDriver(name)
			self._setDisplay(newDisplayClass, isFallback=isFallback, detected=detected)
			if not isFallback:
				if not detected:
					config.conf["braille"]["display"] = newDisplayClass.name
				elif (
					"bluetoothName" in detected.deviceInfo
					or detected.deviceInfo.get("provider") == "bluetooth"
				):
					# As USB devices have priority over Bluetooth, keep a detector running to switch to USB when connected.
					# Note that the detector should always be running in this situation, so we can trigger a rescan.
					self._detector.rescan(bluetooth=False, limitToDevices=[newDisplayClass.name])
				else:
					self._disableDetection()
			return True
		except Exception:
			# For auto display detection, logging an error for every failure is too obnoxious.
			if not detected:
				log.error(f"Error initializing display driver {name!r}", exc_info=True)
			elif bdDetect._isDebug():
				log.debugWarning(f"Couldn't initialize display driver {name!r}", exc_info=True)
			fallbackDisplayClass = _getDisplayDriver(NO_BRAILLE_DISPLAY_NAME)
			# Only initialize the fallback if it is not already set
			if self.display.__class__ != fallbackDisplayClass:
				self._setDisplay(fallbackDisplayClass, isFallback=False)
			return False

	def _switchDisplay(
		self,
		oldDisplay: Optional["BrailleDisplayDriver"],
		newDisplayClass: Type["BrailleDisplayDriver"],
		**kwargs,
	) -> "BrailleDisplayDriver":
		sameDisplayReInit = newDisplayClass == oldDisplay.__class__
		if sameDisplayReInit:
			# This is the same driver as was already set, so just re-initialize it.
			log.debug(f"Reinitializing {newDisplayClass.name!r} braille display")
			oldDisplay.terminate()
			newDisplay = oldDisplay
		else:
			newDisplay = newDisplayClass.__new__(newDisplayClass)
		extensionPoints.callWithSupportedKwargs(newDisplay.__init__, **kwargs)
		if not sameDisplayReInit:
			if oldDisplay:
				log.debug(f"Switching braille display from {oldDisplay.name!r} to {newDisplay.name!r}")
				try:
					oldDisplay.terminate()
				except Exception:
					log.error("Error terminating previous display driver", exc_info=True)
		newDisplay.initSettings()
		return newDisplay

	def _setDisplay(
		self,
		newDisplayClass: Type["BrailleDisplayDriver"],
		isFallback: bool = False,
		detected: typing.Optional[bdDetect.DeviceMatch] = None,
	):
		kwargs = {}
		if detected:
			kwargs["port"] = detected
		else:
			# See if the user has defined a specific port to connect to
			try:
				kwargs["port"] = config.conf["braille"][newDisplayClass.name]["port"]
			except KeyError:
				pass

		if bdDetect._isDebug() and detected:
			log.debug(f"Possibly detected display {newDisplayClass.description!r}")
		oldDisplay = self.display
		newDisplay = self._switchDisplay(oldDisplay, newDisplayClass, **kwargs)
		self.display = newDisplay
		log.info(
			f"Loaded braille display driver {newDisplay.name!r}, current display has {newDisplay.numCells} cells.",
		)
		displayChanged.notify(display=newDisplay, isFallback=isFallback, detected=detected)
		queueHandler.queueFunction(queueHandler.eventQueue, self.initialDisplay)

	def _onBrailleViewerChangedState(self, created):
		if created:
			self._updateDisplay()
		log.debug("Braille Viewer enabled: {}".format(self.enabled))

	def _updateDisplay(self):
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		self._cursorBlinkUp = showCursor = config.conf["braille"]["showCursor"]
		self._displayWithCursor()
		if self._cursorPos is None or not showCursor:
			return
		cursorShouldBlink = config.conf["braille"]["cursorBlink"]
		blinkRate = config.conf["braille"]["cursorBlinkRate"]
		if cursorShouldBlink and blinkRate:
			self._cursorBlinkTimer = gui.NonReEntrantTimer(self._blink)
			# This is called from another thread when a display is auto detected.
			# Make sure we start the blink timer from the main thread to avoid wx assertions
			wx.CallAfter(self._cursorBlinkTimer.Start, blinkRate)

	def _normalizeCellArraySize(
		self,
		oldCells: list[int],
		oldCellCount: int,
		oldNumRows: int,
		newCellCount: int,
		newNumRows: int,
	) -> list[int]:
		"""
		Given a list of braille cells of length oldCell Count layed out in sequencial rows of oldNumRows,
		return a list of braille cells of length newCellCount layed out in sequencial rows of newNumRows,
		padding or truncating the rows and columns as necessary.
		"""
		oldNumCols = oldCellCount // oldNumRows
		newNumCols = newCellCount // newNumRows
		if len(oldCells) < oldCellCount:
			log.warning("Braille cells are shorter than the display size. Padding with blank cells.")
			oldCells.extend([0] * (oldCellCount - len(oldCells)))
		newCells = []
		if newCellCount != oldCellCount or newNumRows != oldNumRows:
			for rowIndex in range(newNumRows):
				if rowIndex < oldNumRows:
					start = rowIndex * oldNumCols
					rowLen = min(oldNumCols, newNumCols)
					end = start + rowLen
					row = oldCells[start:end]
					if rowLen < newNumCols:
						row.extend([0] * (newNumCols - rowLen))
				else:
					row = [0] * newNumCols
				newCells.extend(row)
		else:
			newCells = oldCells
		return newCells

	def _writeCells(self, cells: List[int]):
		handlerCellCount = self.displaySize
		pre_writeCells.notify(cells=cells, rawText=self._rawText, currentCellCount=handlerCellCount)
		displayCellCount = self.display.numCells
		if not displayCellCount:
			# No physical display to write to
			return
		# Braille displays expect cells to be padded up to displayCellCount.
		# However, the braille handler uses handlerCellCount to calculate the number of cells.
		# number of rows / columns may also differ.
		cells = self._normalizeCellArraySize(
			cells,
			handlerCellCount,
			self.displayDimensions.numRows,
			displayCellCount,
			self.display.numRows,
		)
		if not self.display.isThreadSafe:
			try:
				self.display.display(cells)
			except:  # noqa: E722
				log.error("Error displaying cells. Disabling display", exc_info=True)
				self.handleDisplayUnavailable()
			return
		with self.queuedWriteLock:
			alreadyQueued: Optional[List[int]] = self.queuedWrite
			self.queuedWrite = cells
		# If a write was already queued, we don't need to queue another;
		# we just replace the data.
		# This means that if multiple writes occur while an earlier write is still in progress,
		# we skip all but the last.
		if not alreadyQueued and not self.display._awaitingAck:
			# Queue a call to the background thread.
			self._writeCellsInBackground()

	def _writeCellsInBackground(self):
		"""Writes cells to a braille display in the background by queuing a function to the i/o thread."""
		hwIo.bgThread.queueAsApc(self._bgThreadExecutor)

	def _displayWithCursor(self):
		if not self._cells:
			return
		cells = list(self._cells)
		if self._cursorPos is not None and self._cursorBlinkUp:
			if self.getTether() == TetherTo.FOCUS.value:
				cells[self._cursorPos] |= config.conf["braille"]["cursorShapeFocus"]
			else:
				cells[self._cursorPos] |= config.conf["braille"]["cursorShapeReview"]
		self._writeCells(cells)

	def _blink(self):
		self._cursorBlinkUp = not self._cursorBlinkUp
		self._displayWithCursor()

	def update(self):
		cells = self.buffer.windowBrailleCells
		self._rawText = self.buffer.windowRawText
		if log.isEnabledFor(log.IO):
			log.io("Braille window dots: %s" % formatCellsForLog(cells))
		# cells might not be the full length of the display.
		# Therefore, pad it with spaces to fill the display.
		self._cells = cells + [0] * (self.displaySize - len(cells))
		self._cursorPos = self.buffer.cursorWindowPos
		self._updateDisplay()

	def scrollForward(self):
		self.buffer.scrollForward()
		if self.buffer is self.messageBuffer:
			self._resetMessageTimer()
		if self._autoScrollCallLater:
			# Reset the timer.
			self._resetAutoScroll()

	def scrollBack(self):
		self.buffer.scrollBack()
		if self.buffer is self.messageBuffer:
			self._resetMessageTimer()
		if self._autoScrollCallLater:
			# Reset the timer.
			self._resetAutoScroll()

	def routeTo(self, windowPos):
		self.autoScroll(enable=False)
		self.buffer.routeTo(windowPos)
		if self.buffer is self.messageBuffer:
			self._dismissMessage()

	def getTextInfoForWindowPos(self, windowPos):
		if self.buffer is not self.mainBuffer:
			return None
		return self.buffer.getTextInfoForWindowPos(windowPos)

	def message(self, text):
		"""Display a message to the user which times out after a configured interval.
		The timeout will be reset if the user scrolls the display.
		The message will be dismissed immediately if the user presses a cursor routing key.
		If a key is pressed the message will be dismissed by the next text being written to the display.
		@postcondition: The message is displayed.
		"""
		if (
			(not self.enabled and _decide_disabledIncludesMessages.decide())
			or config.conf["braille"]["showMessages"] == ShowMessages.DISABLED
			or text is None
			or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value
		):
			return
		_pre_showBrailleMessage.notify()
		self.autoScroll(enable=False)
		if self.buffer is self.messageBuffer:
			self.buffer.clear()
		else:
			self.buffer = self.messageBuffer
		region = TextRegion(text)
		region.update()
		self.buffer.regions.append(region)
		self.buffer.update()
		self.update()
		self._resetMessageTimer()
		self._keyCountForLastMessage = keyboardHandler.keyCounter

	def _resetMessageTimer(self):
		"""Reset the message timeout.
		@precondition: A message is currently being displayed.
		"""
		if config.conf["braille"]["showMessages"] == ShowMessages.SHOW_INDEFINITELY:
			return
		# Configured timeout is in seconds.
		timeout = config.conf["braille"]["messageTimeout"] * 1000
		if self._messageCallLater:
			self._messageCallLater.Restart(timeout)
		else:
			self._messageCallLater = wx.CallLater(timeout, self._dismissMessage)

	def _dismissMessage(self, shouldUpdate: bool = True):
		"""Dismiss the current message.
		@param shouldUpdate: Whether to call update after dismissing.
		@precondition: A message is currently being displayed.
		@postcondition: The display returns to the main buffer.
		"""
		self.buffer.clear()
		self.buffer = self.mainBuffer
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		if shouldUpdate:
			self.update()
		_post_dismissBrailleMessage.notify()

	def autoScroll(self, enable: bool) -> None:
		"""
		Enable or disable automatic scroll.

		:param enable: ``True`` if automatic scroll should be enabled, ``False`` otherwise.
		"""

		if not self.enabled:
			return
		if enable and self._autoScrollCallLater is None:
			self._autoScrollCallLater = wx.CallLater(self._calculateAutoScrollTimeout(), self.scrollForward)
		elif not enable and self._autoScrollCallLater is not None:
			self._autoScrollCallLater.Stop()
			self._autoScrollCallLater = None

	def _calculateAutoScrollTimeout(self) -> int:
		"""
		Calculate the timeout for automatic scroll.

		:return: The number of milliseconds to wait until the next scroll.
		"""

		autoScrollRate = config.conf["braille"]["autoScrollRate"]
		return int((self.displaySize / autoScrollRate) * 1000)

	def _resetAutoScroll(self) -> None:
		"""
		Reset autoScroll.
		"""

		self._autoScrollCallLater.Restart()

	def handleGainFocus(self, obj: "NVDAObject", shouldAutoTether: bool = True) -> None:
		if not self.enabled or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value:
			return
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		if shouldAutoTether:
			self.setTether(TetherTo.FOCUS.value, auto=True)
		if self._tether != TetherTo.FOCUS.value:
			return
		if (
			getattr(obj, "treeInterceptor", None)
			and not obj.treeInterceptor.passThrough
			and obj.treeInterceptor.isReady
		):
			obj = obj.treeInterceptor
		self._doNewObject(
			itertools.chain(
				getFocusContextRegions(obj, oldFocusRegions=self.mainBuffer.regions),
				getFocusRegions(obj),
			),
		)

	def _doNewObject(self, regions):
		self.autoScroll(enable=False)
		self.mainBuffer.clear()
		focusToHardLeftSet = False
		for region in regions:
			if (
				self.getTether() == TetherTo.FOCUS.value
				and config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_CHANGEDCONTEXT
			):
				# Check focusToHardLeft for every region.
				# If noone of the regions has focusToHardLeft set to True, set it for the first focus region.
				if region.focusToHardLeft:
					focusToHardLeftSet = True
				elif not focusToHardLeftSet and getattr(region, "_focusAncestorIndex", None) is None:
					# Going to display a new object with the same ancestry as the previously displayed object.
					# So, set focusToHardLeft on this region
					# For example, this applies when you are in a list and start navigating through it
					region.focusToHardLeft = True
					focusToHardLeftSet = True
			self.mainBuffer.regions.append(region)
		self.mainBuffer.update()
		# Last region should receive focus.
		self.mainBuffer.focus(region)
		self.scrollToCursorOrSelection(region)
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter > self._keyCountForLastMessage:
			self._dismissMessage()

	def handleCaretMove(
		self,
		obj: "NVDAObject",
		shouldAutoTether: bool = True,
	) -> None:
		if not self.enabled or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value:
			return
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		prevTether = self._tether
		if shouldAutoTether:
			self.setTether(TetherTo.FOCUS.value, auto=True)
		if self._tether != TetherTo.FOCUS.value:
			return
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == obj:
			region.pendingCaretUpdate = True
			self._regionsPendingUpdate.add(region)
		elif prevTether == TetherTo.REVIEW.value:
			# The caret moved in a different object than the review position.
			self._doNewObject(getFocusRegions(obj, review=False))

	def _handlePendingUpdate(self):
		"""When any region is pending an update, updates the region and the braille display."""
		if not self._regionsPendingUpdate:
			return
		try:
			scrollTo: Optional[TextInfoRegion] = None
			self.mainBuffer.saveWindow()
			for region in self._regionsPendingUpdate:
				from treeInterceptorHandler import TreeInterceptor

				if isinstance(region.obj, TreeInterceptor) and not region.obj.isAlive:
					log.debug("Skipping region update for died tree interceptor")
					continue
				try:
					region.update()
				except Exception:
					log.debugWarning(
						f"Region update failed for {region}, object probably died",
						exc_info=True,
					)
					continue
				if isinstance(region, TextInfoRegion) and region.pendingCaretUpdate:
					scrollTo = region
					region.pendingCaretUpdate = False
			self.mainBuffer.update()
			self.mainBuffer.restoreWindow()
			if scrollTo is not None:
				self.scrollToCursorOrSelection(scrollTo)
			if self.buffer is self.mainBuffer:
				self.update()
			elif (
				self.buffer is self.messageBuffer
				and keyboardHandler.keyCounter > self._keyCountForLastMessage
			):
				self._dismissMessage()
		finally:
			self._regionsPendingUpdate.clear()

	def scrollToCursorOrSelection(self, region):
		if region.brailleCursorPos is not None:
			self.mainBuffer.scrollTo(region, region.brailleCursorPos)
		elif not isinstance(region, TextInfoRegion) or not region.obj.isTextSelectionAnchoredAtStart:
			# It is unknown where the selection is anchored, or it is anchored at the end.
			if region.brailleSelectionStart is not None:
				self.mainBuffer.scrollTo(region, region.brailleSelectionStart)
		elif region.brailleSelectionEnd is not None:
			# The selection is anchored at the start.
			self.mainBuffer.scrollTo(region, region.brailleSelectionEnd - 1)

	# #6862: The value change of a progress bar change often goes together with changes of other objects in the dialog,
	# e.g. the time remaining. Therefore, update the dialog when a contained progress bar changes.
	def _handleProgressBarUpdate(
		self,
		obj: "NVDAObject",
	) -> None:
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		oldTime = getattr(self, "_lastProgressBarUpdateTime", None)
		newTime = time.time()
		if oldTime and newTime - oldTime < 1:
			# Fetching dialog text is expensive, so update at most once a second.
			return
		self._lastProgressBarUpdateTime = newTime
		for obj in reversed(api.getFocusAncestors()[:-1]):
			if obj.role == controlTypes.Role.DIALOG:
				self.handleUpdate(obj)
				return

	def handleUpdate(self, obj: "NVDAObject") -> None:
		if not self.enabled:
			return
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		# Optimisation: It is very likely that it is the focus object that is being updated.
		# If the focus object is in the braille buffer, it will be the last region, so scan the regions backwards.
		for region in reversed(list(self.mainBuffer.visibleRegions)):
			if hasattr(region, "obj") and region.obj == obj:
				break
		else:
			# No region for this object.
			# There are some objects that require special update behavior even if they have no region.
			# This only applies when tethered to focus, because tethering to review shows only one object at a time,
			# which always has a braille region associated with it.
			if self._tether != TetherTo.FOCUS.value:
				return
			# Late import to avoid circular import.
			from NVDAObjects import NVDAObject

			if (
				isinstance(obj, NVDAObject)
				and obj.role == controlTypes.Role.PROGRESSBAR
				and obj.isInForeground
			):
				self._handleProgressBarUpdate(obj)
			return
		self._regionsPendingUpdate.add(region)

	def handleReviewMove(self, shouldAutoTether=True):
		if not self.enabled or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value:
			return
		reviewPos = api.getReviewPosition()
		if shouldAutoTether:
			self.setTether(TetherTo.REVIEW.value, auto=True)
		if self._tether != TetherTo.REVIEW.value:
			return
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == reviewPos.obj:
			region.pendingCaretUpdate = True
			self._regionsPendingUpdate.add(region)
		else:
			# We're reviewing a different object.
			self._doNewObject(getFocusRegions(reviewPos.obj, review=True))

	def initialDisplay(self):
		if not self.enabled or not api.getDesktopObject():
			# Braille is disabled or focus/review hasn't yet been initialised.
			return
		try:
			if self.getTether() == TetherTo.FOCUS.value:
				self.handleGainFocus(api.getFocusObject(), shouldAutoTether=False)
			else:
				self.handleReviewMove(shouldAutoTether=False)
		except Exception:
			# #8877: initialDisplay might fail because NVDA tries to focus
			# an object for which property fetching raises an exception.
			log.debugWarning("Error in initial display", exc_info=True)

	def handlePostConfigProfileSwitch(self):
		display = config.conf["braille"]["display"]
		# #7459: the syncBraille has been dropped in favor of the native hims driver.
		# Migrate to renamed drivers as smoothly as possible.
		newDriverName = RENAMED_DRIVERS.get(display)
		if newDriverName:
			display = config.conf["braille"]["display"] = newDriverName
		if (
			self.display is None
			# Do not choose a new display if:
			or not (
				# The display in the new profile is equal to the last requested display name
				display == self._lastRequestedDisplayName
				# or the new profile uses auto detection, which supports detection of the currently active display.
				or (
					display == AUTO_DISPLAY_NAME
					and bdDetect.driverIsEnabledForAutoDetection(self.display.name)
				)
			)
		):
			self.setDisplayByName(display)
		elif (
			# Auto detection should be active
			display == AUTO_DISPLAY_NAME
			and self._detector is not None
			# And the current display should be no braille.
			# If not, there is an active detector for the current driver
			# to switch from bluetooth to USB.
			and self.display.name == NO_BRAILLE_DISPLAY_NAME
		):
			self._detector._limitToDevices = bdDetect.getBrailleDisplayDriversEnabledForDetection()

		if (configuredTether := config.conf["braille"]["tetherTo"]) != TetherTo.AUTO.value:
			self._tether = configuredTether

		tableName = config.conf["braille"]["translationTable"]
		# #6140: Migrate to new table names as smoothly as possible.
		newTableName = brailleTables.RENAMED_TABLES.get(tableName)
		if newTableName:
			tableName = config.conf["braille"]["translationTable"] = newTableName
		if config.conf["braille"]["translationTable"] == "auto":
			table = brailleTables.getDefaultTableForCurLang(brailleTables.TableType.OUTPUT)
		else:
			table = tableName
		if tableName != self._table.fileName:
			try:
				self._table = brailleTables.getTable(table)
			except LookupError:
				log.error(
					f"Invalid translation table ({tableName}), falling back to default ({FALLBACK_TABLE}).",
				)
				self._table = brailleTables.getTable(FALLBACK_TABLE)

	def handleDisplayUnavailable(self):
		"""Called when the braille display becomes unavailable.
		This logs an error and disables the display.
		This is called when displaying cells raises an exception,
		but drivers can also call it themselves if appropriate.
		"""
		log.error("Braille display unavailable. Disabling", exc_info=True)
		newDisplay = (
			AUTO_DISPLAY_NAME
			if config.conf["braille"]["display"] == AUTO_DISPLAY_NAME
			else NO_BRAILLE_DISPLAY_NAME
		)
		self.setDisplayByName(newDisplay, isFallback=True)

	def _enableDetection(
		self,
		usb: bool = True,
		bluetooth: bool = True,
		limitToDevices: Optional[List[str]] = None,
		preferredDevice: bdDetect.DriverAndDeviceMatch | None = None,
	):
		"""Enables automatic detection of braille displays.
		When auto detection is already active, this will force a rescan for devices.
		This should also be executed when auto detection should be resumed due to loss of display connectivity.
		In that case, it is triggered by L{setDisplayByname}.
		:param usb: Whether to scan for USB devices
		:param bluetooth: Whether to scan for Bluetooth devices.
		:param limitToDevices: An optional list of driver names a scan should be limited to.
			This is used when a Bluetooth device is detected, in order to switch to USB
			when an USB device for the same driver is found.
			``None`` if no driver filtering should occur.
		:param preferredDevice: An optional preferred device to use for detection.
			this device is attempted to be used before a scan is started.
		"""
		self.setDisplayByName(NO_BRAILLE_DISPLAY_NAME, isFallback=True)
		if self._detector:
			self._detector.rescan(
				usb=usb,
				bluetooth=bluetooth,
				limitToDevices=limitToDevices,
				preferredDevice=preferredDevice,
			)
			return
		config.conf["braille"]["display"] = AUTO_DISPLAY_NAME
		self._detector = bdDetect._Detector()
		self._detector._queueBgScan(
			usb=usb,
			bluetooth=bluetooth,
			limitToDevices=limitToDevices,
			preferredDevice=preferredDevice,
		)

	def _disableDetection(self):
		"""Disables automatic detection of braille displays."""
		if self._detector:
			self._detector.terminate()
			self._detector = None

	def _bgThreadExecutor(self, param: int):
		"""Executed as APC when cells have to be written to a display asynchronously."""
		if not self.display:
			# Sometimes, the bg thread executor is triggered when a display is not fully initialized.
			# For example, this happens when handling an ACK during initialisation.
			# We can safely ignore this.
			return
		if self.display._awaitingAck:
			# Do not write cells when we are awaiting an ACK
			return
		with self.queuedWriteLock:
			data: Optional[List[int]] = self.queuedWrite
			self.queuedWrite = None
		if not data:
			return
		try:
			self.display.display(data)
		except:  # noqa: E722
			log.error("Error displaying cells. Disabling display", exc_info=True)
			self.handleDisplayUnavailable()
		else:
			if self.display.receivesAckPackets:
				self.display._awaitingAck = True
				SECOND_TO_MS = 1000
				hwIo.bgThread.setWaitableTimer(
					self.ackTimerHandle,
					# Wait twice the display driver timeout for acknowledgement packets
					# Note: timeout is in seconds whereas setWaitableTimer expects milliseconds
					int(self.display.timeout * 2 * SECOND_TO_MS),
					self._ackTimeoutResetter,
				)

	def _ackTimeoutResetter(self, param: int):
		if self.display and self.display.receivesAckPackets and self.display._awaitingAck:
			log.debugWarning(f"Waiting for {self.display.name} ACK packet timed out")
			self.display._awaitingAck = False
			self._writeCellsInBackground()
