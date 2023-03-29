# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2021 NV Access Limited, James Teh, Michael Curran, Leonard de Ruijter, Reef Turner,
# Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import typing

import appModuleHandler
import api
import controlTypes
import versionInfo
from NVDAObjects.IAccessible import IAccessible
from baseObject import ScriptableObject
import gui
from scriptHandler import script
import speech
import textInfos
import braille
import config
from logHandler import log

if typing.TYPE_CHECKING:
	import inputCore


nvdaMenuIaIdentity = None

class NvdaDialog(IAccessible):
	"""Fix to ensure NVDA message dialogs get reported when they pop up.
	"""

	def _get_presentationType(self):
		presType = super(NvdaDialog, self).presentationType
		# Sometimes, NVDA message dialogs briefly report the invisible state
		# after they're focused.
		# This causes them to be treated as unavailable and they are thus not reported.
		# If this dialog is in the foreground, treat it as content.
		if presType == self.presType_unavailable and self == api.getForegroundObject():
			return self.presType_content
		return presType


class NvdaDialogEmptyDescription(IAccessible):
	"""Fix to ensure the NVDA settings dialog does not run getDialogText including panel descriptions
		when alt+tabbing back to a focused control on a panel with a description. This would result in the
		description being spoken twice.
	"""

	def _get_description(self):
		"""Override the description property (because we can't override the classmethod getDialogText)
			However this will do to ensure that the dialog is described as we wish.
		"""
		return ""


# Translators: The name of a category of NVDA commands.
SCRCAT_PYTHON_CONSOLE = _("Python Console")


class NvdaPythonConsoleUIOutputClear(ScriptableObject):

	# Allow the bound gestures to be edited through the Input Gestures dialog (see L{gui.prePopup})
	isPrevFocusOnNvdaPopup = True

	@script(
		gesture="kb:control+l",
		# Translators: Description of a command to clear the Python Console output pane
		description=_("Clear the output pane"),
		category=SCRCAT_PYTHON_CONSOLE,
	)
	def script_clearOutput(self, gesture: "inputCore.InputGesture"):
		from pythonConsole import consoleUI
		consoleUI.clear()


class NvdaPythonConsoleUIOutputCtrl(ScriptableObject):

	# Allow the bound gestures to be edited through the Input Gestures dialog (see L{gui.prePopup})
	isPrevFocusOnNvdaPopup = True

	@script(
		gesture="kb:alt+downArrow",
		# Translators: Description of a command to move to the next result in the Python Console output pane
		description=_("Move to the next result"),
		category=SCRCAT_PYTHON_CONSOLE
	)
	def script_moveToNextResult(self, gesture: "inputCore.InputGesture"):
		self._resultNavHelper(direction="next", select=False)

	@script(
		gesture="kb:alt+upArrow",
		# Translators: Description of a command to move to the previous result
		# in the Python Console output pane
		description=_("Move to the previous result"),
		category=SCRCAT_PYTHON_CONSOLE
	)
	def script_moveToPrevResult(self, gesture: "inputCore.InputGesture"):
		self._resultNavHelper(direction="previous", select=False)

	@script(
		gesture="kb:alt+downArrow+shift",
		# Translators: Description of a command to select from the current caret position to the end
		# of the current result in the Python Console output pane
		description=_("Select until the end of the current result"),
		category=SCRCAT_PYTHON_CONSOLE
	)
	def script_selectToResultEnd(self, gesture: "inputCore.InputGesture"):
		self._resultNavHelper(direction="next", select=True)

	@script(
		gesture="kb:alt+shift+upArrow",
		# Translators: Description of a command to select from the current caret position to the start
		# of the current result in the Python Console output pane
		description=_("Select until the start of the current result"),
		category=SCRCAT_PYTHON_CONSOLE
	)
	def script_selectToResultStart(self, gesture: "inputCore.InputGesture"):
		self._resultNavHelper(direction="previous", select=True)

	def _resultNavHelper(self, direction: str = "next", select: bool = False):
		from pythonConsole import consoleUI
		startPos, endPos = consoleUI.outputCtrl.GetSelection()
		if self.isTextSelectionAnchoredAtStart:
			curPos = endPos
		else:
			curPos = startPos
		if direction == "previous":
			for pos in reversed(consoleUI.outputPositions):
				if pos < curPos:
					break
			else:
				# Translators: Reported when attempting to move to the previous result in the Python Console
				# output pane while there is no previous result.
				speech.speakMessage(_("Top"))
				return
		elif direction == "next":
			for pos in consoleUI.outputPositions:
				if pos > curPos:
					break
			else:
				# Translators: Reported when attempting to move to the next result in the Python Console
				# output pane while there is no next result.
				speech.speakMessage(_("Bottom"))
				return
		else:
			raise ValueError(u"Unexpected direction: {!r}".format(direction))
		if select:
			consoleUI.outputCtrl.Freeze()
			anchorPos = startPos if self.isTextSelectionAnchoredAtStart else endPos
			consoleUI.outputCtrl.SetSelection(anchorPos, pos)
			consoleUI.outputCtrl.Thaw()
			self.detectPossibleSelectionChange()
			self.isTextSelectionAnchoredAtStart = anchorPos < pos
		else:
			consoleUI.outputCtrl.SetSelection(pos, pos)
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		copy = info.copy()
		info.expand(textInfos.UNIT_LINE)
		if (
			copy.move(textInfos.UNIT_CHARACTER, 4, endPoint="end") == 4
			and copy.text == ">>> "
		):
			info.move(textInfos.UNIT_CHARACTER, 4, endPoint="start")
		speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET)


class AppModule(appModuleHandler.AppModule):
	# The configuration profile that has been previously edited.
	# This ought to be a class property.
	oldProfile = None

	@classmethod
	def handlePossibleProfileSwitch(cls):
		from gui.settingsDialogs import NvdaSettingsDialogActiveConfigProfile as newProfile
		if (cls.oldProfile and newProfile and newProfile != cls.oldProfile):
			# Translators: A message announcing what configuration profile is currently being edited.
			speech.speakMessage(_("Editing profile {profile}").format(profile=newProfile))
		cls.oldProfile = newProfile

	def event_appModule_loseFocus(self):
		self.oldProfile = None

	def isNvdaMenu(self, obj):
		global nvdaMenuIaIdentity
		if not isinstance(obj, IAccessible):
			return False
		if nvdaMenuIaIdentity and obj.IAccessibleIdentity == nvdaMenuIaIdentity:
			return True
		if nvdaMenuIaIdentity is not True:
			return False
		# nvdaMenuIaIdentity is True, so the next menu we encounter is the NVDA menu.
		if obj.role == controlTypes.Role.POPUPMENU:
			nvdaMenuIaIdentity = obj.IAccessibleIdentity
			return True
		return False

	def event_NVDAObject_init(self, obj):
		# It seems that context menus always get the name "context" and this cannot be overridden.
		# Fudge the name of the NVDA system tray menu to make it more friendly.
		if self.isNvdaMenu(obj):
			obj.name=versionInfo.name

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == controlTypes.Role.UNKNOWN and controlTypes.State.INVISIBLE in obj.states:
			return
		nextHandler()

	# Silence invisible unknowns for stateChange as well.
	event_stateChange = event_gainFocus

	def event_foreground(self, obj, nextHandler):
		if not gui.shouldConfigProfileTriggersBeSuspended():
			config.conf.resumeProfileTriggers()
		else:
			self.handlePossibleProfileSwitch()
		nextHandler()

	def event_nameChange(self, obj, nextHandler):
		self.handlePossibleProfileSwitch()
		nextHandler()

	def isNvdaSettingsDialog(self, obj):
		if not isinstance(obj, IAccessible):
			return False
		windowHandle = obj.windowHandle
		from gui.settingsDialogs import NvdaSettingsDialogWindowHandle
		if windowHandle == NvdaSettingsDialogWindowHandle:
			return True
		return False

	def isNvdaPythonConsoleUIInputCtrl(self, obj):
		from pythonConsole import consoleUI
		if not consoleUI:
			return
		return obj.windowHandle == consoleUI.inputCtrl.GetHandle()

	def isNvdaPythonConsoleUIOutputCtrl(self, obj):
		from pythonConsole import consoleUI
		if not consoleUI:
			return
		return obj.windowHandle == consoleUI.outputCtrl.GetHandle()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "#32770" and obj.role == controlTypes.Role.DIALOG:
			clsList.insert(0, NvdaDialog)
			if self.isNvdaSettingsDialog(obj):
				clsList.insert(0, NvdaDialogEmptyDescription)
				return
		if self.isNvdaPythonConsoleUIInputCtrl(obj):
			clsList.insert(0, NvdaPythonConsoleUIOutputClear)
		elif self.isNvdaPythonConsoleUIOutputCtrl(obj):
			clsList.insert(0, NvdaPythonConsoleUIOutputClear)
			clsList.insert(0, NvdaPythonConsoleUIOutputCtrl)
