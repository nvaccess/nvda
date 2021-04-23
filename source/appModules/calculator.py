# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 10 Calculator"""

import appModuleHandler
import api
from NVDAObjects.UIA import UIA
import queueHandler
import ui
import scriptHandler

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

	def event_UIA_notification(self, obj, nextHandler, activityId=None, **kwargs):
		try:
			shouldAnnounceNotification = (
				obj.previous.UIAAutomationId in
				("numberPad", "UnitConverterRootGrid")
			)
		except AttributeError:
			resultElement = api.getForegroundObject().children[1].lastChild
			# Redesigned in 2019 due to introduction of "always on top" i.e. compact overlay mode.
			if resultElement.UIAElement.cachedClassName != "LandmarkTarget":
				resultElement = resultElement.parent.children[1]
			shouldAnnounceNotification = (
				resultElement
				and resultElement.firstChild
				and resultElement.firstChild.UIAAutomationId not in noCalculatorEntryAnnouncements
			)
		# Display updated activity ID seen when entering calculations should be ignored
		# as as it is redundant if speak typed characters is on.
		if shouldAnnounceNotification or activityId != "DisplayUpdated":
			nextHandler()

	# A list of native commands to handle calculator result announcement.
	_calculatorResultGestures = ("kb:enter", "kb:numpadEnter", "kb:escape")

	@scriptHandler.script(gestures=_calculatorResultGestures)
	def script_calculatorResult(self, gesture):
		# To prevent double focus announcement, check where we are.
		focus = api.getFocusObject()
		gesture.send()
		# In redstone, calculator result keeps firing name change,
		# so tell it to do so if and only if enter has been pressed.
		self._shouldAnnounceResult = True
		# Hack: only announce display text when an actual calculator button (usually equals button) is pressed.
		# In redstone, pressing enter does not move focus to equals button.
		if isinstance(focus, UIA):
			if focus.UIAAutomationId in ("CalculatorResults", "CalculatorAlwaysOnTopResults"):
				queueHandler.queueFunction(queueHandler.eventQueue, focus.reportFocus)
			else:
				resultsScreen = api.getForegroundObject().children[1].lastChild
				if isinstance(resultsScreen, UIA) and resultsScreen.UIAElement.cachedClassName == "LandmarkTarget":
					# And no, do not allow focus to move.
					queueHandler.queueFunction(queueHandler.eventQueue, resultsScreen.firstChild.reportFocus)
