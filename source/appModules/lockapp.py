#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import inputCore
import api
import eventHandler
import config
from NVDAObjects.UIA import UIA
from globalCommands import GlobalCommands

"""App module for the Windows 10 lock screen.
The lock screen runs as the logged in user on the default desktop,
so we need to explicitly stop people from accessing/changing things outside of the lock screen.
"""

# Windows 10 lock screen container
class LockAppContainer(UIA):
	# Make sure the user can get to this so they can dismiss the lock screen from a touch screen.
	presentationType=UIA.presType_content

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA) and obj.role==controlTypes.ROLE_PANE and obj.UIAElement.cachedClassName=="LockAppContainer":
			clsList.insert(0,LockAppContainer)

	def event_NVDAObject_init(self, obj):
		if obj.role == controlTypes.ROLE_WINDOW:
			# Stop users from being able to object navigate out of the lock screen.
			obj.parent = None

	SAFE_SCRIPTS = {
		GlobalCommands.script_reportCurrentFocus.__func__,
		GlobalCommands.script_title.__func__,
		GlobalCommands.script_dateTime.__func__,
		GlobalCommands.script_say_battery_status.__func__,
		GlobalCommands.script_navigatorObject_current.__func__,
		GlobalCommands.script_navigatorObject_currentDimensions.__func__,
		GlobalCommands.script_navigatorObject_toFocus.__func__,
		GlobalCommands.script_navigatorObject_moveFocus.__func__,
		GlobalCommands.script_navigatorObject_parent.__func__,
		GlobalCommands.script_navigatorObject_next.__func__,
		GlobalCommands.script_navigatorObject_previous.__func__,
		GlobalCommands.script_navigatorObject_firstChild.__func__,
		GlobalCommands.script_review_activate.__func__,
		GlobalCommands.script_review_top.__func__,
		GlobalCommands.script_review_previousLine.__func__,
		GlobalCommands.script_review_currentLine.__func__,
		GlobalCommands.script_review_nextLine.__func__,
		GlobalCommands.script_review_bottom.__func__,
		GlobalCommands.script_review_previousWord.__func__,
		GlobalCommands.script_review_currentWord.__func__,
		GlobalCommands.script_review_nextWord.__func__,
		GlobalCommands.script_review_startOfLine.__func__,
		GlobalCommands.script_review_previousCharacter.__func__,
		GlobalCommands.script_review_currentCharacter.__func__,
		GlobalCommands.script_review_nextCharacter.__func__,
		GlobalCommands.script_review_endOfLine.__func__,
		GlobalCommands.script_review_sayAll.__func__,
		GlobalCommands.script_braille_scrollBack.__func__,
		GlobalCommands.script_braille_scrollForward.__func__,
		GlobalCommands.script_braille_routeTo.__func__,
		GlobalCommands.script_braille_previousLine.__func__,
		GlobalCommands.script_braille_nextLine.__func__,
		GlobalCommands.script_navigatorObject_nextInFlow.__func__,
		GlobalCommands.script_navigatorObject_previousInFlow.__func__,
		GlobalCommands.script_touch_changeMode.__func__,
		GlobalCommands.script_touch_newExplore.__func__,
		GlobalCommands.script_touch_explore.__func__,
		GlobalCommands.script_touch_hoverUp.__func__,
		GlobalCommands.script_moveMouseToNavigatorObject.__func__,
		GlobalCommands.script_moveNavigatorObjectToMouse.__func__,
		GlobalCommands.script_leftMouseClick.__func__,
		GlobalCommands.script_rightMouseClick.__func__,
	}
	def _inputCaptor(self, gesture):
		script = gesture.script
		if not script:
			return True
		# Only allow specific scripts so people can't touch the clipboard, change NVDA config, etc.
		return script.__func__ in self.SAFE_SCRIPTS

	def event_appModule_gainFocus(self):
		inputCore.manager._captureFunc = self._inputCaptor
		if not config.conf["reviewCursor"]["followFocus"]:
			# Move the review cursor so others can't access its previous position.
			self._oldReviewPos = api.getReviewPosition()
			self._oldReviewObj = self._oldReviewPos.obj
			api.setNavigatorObject(eventHandler.lastQueuedFocusObject)

	def event_appModule_loseFocus(self):
		if not config.conf["reviewCursor"]["followFocus"]:
			api.setReviewPosition(self._oldReviewPos)
			del self._oldReviewPos, self._oldReviewObj
		inputCore.manager._captureFunc = None
