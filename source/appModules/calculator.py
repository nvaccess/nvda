# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2022 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 10 Calculator.
This is also the base app module for Windows 11 Calculator."""

import appModuleHandler
import api
from NVDAObjects.UIA import UIA
import queueHandler
import ui
import scriptHandler
import braille

# #9428: do not announce current values until calculations are done in order to avoid repetitions.
noCalculatorEntryAnnouncements = [
	# Display field with Calculator set to full screen mode.
	"CalculatorResults",
	# In the middle of a calculation expression entry.
	"CalculatorExpression",
	# Results display with Calculator set to compact overlay i.e. always on top mode.
	"CalculatorAlwaysOnTopResults",
	# Calculator expressions with Calculator set to always on top mode.
	"ExpressionContainer",
	# Date range selector.
	"ContentPresenter",
	# Briefly shown when closing date calculation calendar.
	"Light Dismiss",
	# Unit conversion/convert from.
	"Value1",
	# Unit conversion/converts into.
	"Value2",
]


class AppModule(appModuleHandler.AppModule):

	_shouldAnnounceResult = False
	# Name change says the same thing multiple times for some items.
	_resultsCache = ""
	# #13383: for some commands (such as number row keys), NVDA should not announce calculator results.
	_noCalculatorResultsGesturePressed = False

	def event_NVDAObject_init(self, obj):
		if not isinstance(obj, UIA):
			return
		# #11858: version 10.2009 introduces a regression where history and memory items have no names
		# but can be fetched through its children.
		# Resolved in version 10.2109 which is exclusive to Windows 11.
		if not obj.name and obj.parent.UIAAutomationId in ("HistoryListView", "MemoryListView"):
			obj.name = "".join([item.name for item in obj.children])

	def event_nameChange(self, obj, nextHandler):
		if not isinstance(obj, UIA):
			return
		# No, announce value changes immediately except for calculator results and expressions.
		if (
			obj.UIAAutomationId in noCalculatorEntryAnnouncements
			or obj.UIAElement.cachedClassName == "LandmarkTarget"
		):
			self._shouldAnnounceResult = False
		# For the rest:
		elif (
			obj.UIAAutomationId not in noCalculatorEntryAnnouncements
			and obj.name != self._resultsCache
		):
			# For unit conversion, both name change and notification events are fired,
			# although UIA notification event presents much better messages.
			# For date calculation, live region change event is also fired for difference between dates.
			if obj.UIAAutomationId != "DateDiffAllUnitsResultLabel":
				ui.message(obj.name)
			self._resultsCache = obj.name
		if not self._shouldAnnounceResult:
			return
		self._shouldAnnounceResult = False
		nextHandler()

	def event_UIA_notification(self, obj, nextHandler, displayString=None, activityId=None, **kwargs):
		# When no results shortcuts such as number row keys are pressed, display content will be announced.
		# #13383: it might be possible that the next command is a calculation shortcut such as S for sine.
		# Therefore, clear no result gestures flag from the app module while storing a copy of the flag here.
		# The event handler copy is used to handle the overall notification announcement later.
		doNotAnnounceCalculatorResults = self._noCalculatorResultsGesturePressed
		self._noCalculatorResultsGesturePressed = False
		calculatorVersion = int(self.productVersion.split(".")[0])
		# #12268: for "DisplayUpdated", announce display strings in braille  no matter what they are.
		# There are other activity Id's such as "MemorySlotAdded" and "MemoryCleared"
		# but they do not involve number entry.
		# Therefore, only handle the below activity Id.
		if activityId == "DisplayUpdated":
			braille.handler.message(displayString)
			resultElement = api.getForegroundObject().children[1].lastChild
			# Descend one more time in Windows 11 Calculator.
			if calculatorVersion >= 11:
				resultElement = resultElement.firstChild
			# Redesigned in 2019 due to introduction of "always on top" i.e. compact overlay mode.
			if resultElement.UIAElement.cachedClassName != "LandmarkTarget":
				resultElement = resultElement.parent.children[1]
			# Display string announcement is redundant if speak typed characters is on.
			if (
				resultElement
				and resultElement.firstChild
				and resultElement.firstChild.UIAAutomationId in noCalculatorEntryAnnouncements
				and doNotAnnounceCalculatorResults
			):
				return
		nextHandler()

	# A list of native commands to handle calculator result announcement.
	_calculatorResultGestures = (
		"kb:enter",
		"kb:numpadEnter",
		"kb:escape",
		"kb:delete",
		"kb:numpadDelete"
	)

	@scriptHandler.script(gestures=_calculatorResultGestures)
	def script_calculatorResult(self, gesture):
		# To prevent double focus announcement, check where we are.
		focus = api.getFocusObject()
		gesture.send()
		# #13383: later Calculator releases use UIA notification event to announce results.
		# While the exact version that introduced UIA notification event cannot be found easily,
		# it is definitely used in version 10.1908 and later.
		calculatorVersion = [int(version) for version in self.productVersion.split(".")[:2]]
		if calculatorVersion >= [10, 1908]:
			return
		# In redstone, calculator result keeps firing name change,
		# so tell it to do so if and only if enter has been pressed.
		self._shouldAnnounceResult = True
		# Hack: only announce display text when an actual calculator button (usually equals button) is pressed.
		# In redstone, pressing enter does not move focus to equals button.
		if isinstance(focus, UIA):
			if focus.UIAAutomationId in ("CalculatorResults", "CalculatorAlwaysOnTopResults"):
				queueHandler.queueFunction(queueHandler.eventQueue, ui.message, focus.name)
			else:
				resultsScreen = api.getForegroundObject().children[1].lastChild
				if isinstance(resultsScreen, UIA) and resultsScreen.UIAElement.cachedClassName == "LandmarkTarget":
					# And no, do not allow focus to move.
					queueHandler.queueFunction(queueHandler.eventQueue, ui.message, resultsScreen.firstChild.name)

	# Handle both number row and numpad with num lock on.
	@scriptHandler.script(
		gestures=[f"kb:{i}" for i in range(10)]
		+ [f"kb:numLockNumpad{i}" for i in range(10)]
	)
	def script_doNotAnnounceCalculatorResults(self, gesture):
		gesture.send()
		self._noCalculatorResultsGesturePressed = True
