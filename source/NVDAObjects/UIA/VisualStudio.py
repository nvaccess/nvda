# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited, Leonard de Ruijter

"""
Object overlay classes for Visual Studio components
available in Visual Studio and SQL Server Management Studio.
"""

from . import UIA
import speech
import braille
import api


class IntelliSenseItem(UIA):

	def _get_name(self):
		return self.UIAElement.cachedAutomationID

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


def findExtraOverlayClasses(obj, clsList):
	if obj.UIAAutomationId in _INTELLISENSE_LIST_AUTOMATION_IDS:
		clsList.insert(0, IntelliSenseList)
	elif isinstance(obj.parent, IntelliSenseList) and obj.UIAElement.cachedClassName == "IntellisenseMenuItem":
		clsList.insert(0, IntelliSenseItem)
	elif (
		obj.UIAElement.cachedClassName == "LiveTextBlock"
		and obj.previous
		and isinstance(obj.previous.previous, IntelliSenseList)
	):
		clsList.insert(0, IntelliSenseLiveRegion)
