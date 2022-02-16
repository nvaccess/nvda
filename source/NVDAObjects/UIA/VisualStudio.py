# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020-2022 NV Access Limited, Leonard de Ruijter

"""
Object overlay classes for Visual Studio components
available in Visual Studio and SQL Server Management Studio.
"""

from . import UIA, ToolTip
import speech
import braille
import api
import time


class IntelliSenseItem(UIA):

	def _get_name(self):
		return self.UIAAutomationId

	def event_UIA_elementSelected(self):
		# Cancel speech to have speech announce the selection as soon as possible.
		# This is needed because L{reportFocus} does not cancel speech.
		# Therefore, if speech wouldn't be cancelled,
		# selection announcements would queue up when changing selection rapidly.
		speech.cancelSpeech()
		api.setNavigatorObject(self, isFocus=True)
		self.reportFocus()
		# Display results as flash messages.
		braille.handler.message(braille.getPropertiesBraille(
			name=self.name, role=self.role, positionInfo=self.positionInfo, description=self.description
		))


class IntelliSenseList(UIA):
	...


class IntelliSenseLiveRegion(UIA):
	"""
	Visual Studio uses both Intellisense menu item objects and a live region
	to communicate Intellisense selections.
	NVDA uses the menu item approach and therefore the live region provides doubled information
	and is disabled.
	"""

	_shouldAllowUIALiveRegionChangeEvent = False


_INTELLISENSE_LIST_AUTOMATION_IDS = {
	"listBoxCompletions",
	"CompletionList"
}


class CompletionToolTip(ToolTip):
	""" A tool tip for which duplicate open events can be fired.
	"""

	#: Keeps track of the last ToolTipOpened event (text, time)
	_lastToolTipOpenedInfo = (None, None)
	#: The duplicate tooltip events will be dropped within this time window
	_preventDuplicateToolTipSeconds = 0.2

	def event_UIA_toolTipOpened(self):
		oldText, oldTime = self._lastToolTipOpenedInfo
		newText = self.name
		newTime = time.time()
		self.__class__._lastToolTipOpenedInfo = (newText, newTime)
		withinPossibleDupToolTipTimeWindow = (
			oldTime is not None
			and (newTime - oldTime) < self._preventDuplicateToolTipSeconds
		)
		if newText == oldText and withinPossibleDupToolTipTimeWindow:
			# Tool-tip event suspected to be a duplicate, drop the event.
			# - Users attempting to rapidly re-announce tool-tips may
			#   have the announcement erroneously  suppressed
			# - Users on slower systems (or systems under load) may still
			#   receive duplicate announcements
			return
		super().event_UIA_toolTipOpened()


def findExtraOverlayClasses(obj, clsList):
	if obj.UIAAutomationId in _INTELLISENSE_LIST_AUTOMATION_IDS:
		clsList.insert(0, IntelliSenseList)
	elif obj.UIAElement.cachedClassName == "IntellisenseMenuItem" and isinstance(obj.parent, IntelliSenseList):
		clsList.insert(0, IntelliSenseItem)
	elif (
		obj.UIAElement.cachedClassName == "LiveTextBlock"
		and obj.previous
		and isinstance(obj.previous.previous, IntelliSenseList)
	):
		clsList.insert(0, IntelliSenseLiveRegion)
	elif obj.UIAAutomationId == "completion tooltip":
		clsList.insert(0, CompletionToolTip)
