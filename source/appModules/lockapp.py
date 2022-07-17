# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Callable, Optional
import appModuleHandler
import controlTypes
import inputCore
import api
import eventHandler
import config
import NVDAObjects
from NVDAObjects.UIA import UIA
from globalCommands import GlobalCommands

"""App module for the Windows 10 and 11 lock screen.
The lock screen runs as the logged in user on the default desktop,
so we need to explicitly stop people from accessing/changing things outside of the lock screen.
This is done in the api module by utilizing _isSecureObjectWhileLockScreenActivated.
"""


# Windows 10 and 11 lock screen container
class LockAppContainer(UIA):
	# Make sure the user can get to this so they can dismiss the lock screen from a touch screen.
	presentationType=UIA.presType_content


# Any object in the Lock App
class LockAppObject(NVDAObjects.NVDAObject):
	"""
	Prevent users from object navigating outside of the lock screen.
	While usages of `api._isSecureObjectWhileLockScreenActivated` in the api module prevent
	the user from moving to the object, this overlay class prevents reading the objects.
	"""

	def _get_next(self) -> Optional[NVDAObjects.NVDAObject]:
		nextObject = super()._get_next()
		if nextObject and nextObject.appModule.appName == self.appModule.appName:
			return nextObject
		return None

	def _get_previous(self) -> Optional[NVDAObjects.NVDAObject]:
		previousObject = super()._get_previous()
		if previousObject and previousObject.appModule.appName == self.appModule.appName:
			return previousObject
		return None

	def _get_parent(self) -> Optional[NVDAObjects.NVDAObject]:
		parentObject = super()._get_parent()
		if parentObject and parentObject.appModule.appName == self.appModule.appName:
			return parentObject
		return None


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA) and obj.role==controlTypes.Role.PANE and obj.UIAElement.cachedClassName=="LockAppContainer":
			clsList.insert(0,LockAppContainer)
		clsList.insert(0, LockAppObject)

	def event_foreground(self, obj: NVDAObjects.NVDAObject, nextHandler: Callable[[], None]):
		"""Set mouse object explicitly before continuing to the next handler.
		This is to prevent the mouse focus remaining on the desktop when locking the screen.
		"""
		api.setMouseObject(obj)
		nextHandler()

	SAFE_SCRIPTS = {
		GlobalCommands.script_reportCurrentFocus,
		GlobalCommands.script_title,
		GlobalCommands.script_dateTime,
		GlobalCommands.script_say_battery_status,
		GlobalCommands.script_navigatorObject_current,
		GlobalCommands.script_navigatorObject_currentDimensions,
		GlobalCommands.script_navigatorObject_toFocus,
		GlobalCommands.script_navigatorObject_moveFocus,
		GlobalCommands.script_navigatorObject_parent,
		GlobalCommands.script_navigatorObject_next,
		GlobalCommands.script_navigatorObject_previous,
		GlobalCommands.script_navigatorObject_firstChild,
		GlobalCommands.script_navigatorObject_devInfo,
		GlobalCommands.script_review_activate,
		GlobalCommands.script_review_top,
		GlobalCommands.script_review_previousLine,
		GlobalCommands.script_review_currentLine,
		GlobalCommands.script_review_nextLine,
		GlobalCommands.script_review_bottom,
		GlobalCommands.script_review_previousWord,
		GlobalCommands.script_review_currentWord,
		GlobalCommands.script_review_nextWord,
		GlobalCommands.script_review_startOfLine,
		GlobalCommands.script_review_previousCharacter,
		GlobalCommands.script_review_currentCharacter,
		GlobalCommands.script_review_nextCharacter,
		GlobalCommands.script_review_endOfLine,
		GlobalCommands.script_review_sayAll,
		GlobalCommands.script_braille_scrollBack,
		GlobalCommands.script_braille_scrollForward,
		GlobalCommands.script_braille_routeTo,
		GlobalCommands.script_braille_previousLine,
		GlobalCommands.script_braille_nextLine,
		GlobalCommands.script_navigatorObject_nextInFlow,
		GlobalCommands.script_navigatorObject_previousInFlow,
		GlobalCommands.script_touch_changeMode,
		GlobalCommands.script_touch_newExplore,
		GlobalCommands.script_touch_explore,
		GlobalCommands.script_touch_hoverUp,
		GlobalCommands.script_moveMouseToNavigatorObject,
		GlobalCommands.script_moveNavigatorObjectToMouse,
		GlobalCommands.script_leftMouseClick,
		GlobalCommands.script_rightMouseClick,
	}
	def _inputCaptor(self, gesture):
		script = gesture.script
		if not script:
			return True
		# Only allow specific scripts so people can't touch the clipboard, change NVDA config, etc.
		# #9883: script is a bound method, __func__ gives us the underlying function.
		return script.__func__ in self.SAFE_SCRIPTS

	def event_appModule_gainFocus(self):
		inputCore.manager._captureFunc = self._inputCaptor
		if not config.conf["reviewCursor"]["followFocus"]:
			# Move the review cursor so others can't access its previous position.
			self._oldReviewPos = api.getReviewPosition()
			self._oldReviewObj = self._oldReviewPos.obj
			api.setNavigatorObject(eventHandler.lastQueuedFocusObject, isFocus=True)

	def event_appModule_loseFocus(self):
		if not config.conf["reviewCursor"]["followFocus"]:
			api.setReviewPosition(self._oldReviewPos)
			del self._oldReviewPos, self._oldReviewObj
		inputCore.manager._captureFunc = None
