# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Any,
	Callable,
	List,
)

import appModuleHandler
import api
import config
import controlTypes
import eventHandler
import inputCore
from logHandler import log
from NVDAObjects import NVDAObject
from NVDAObjects.lockscreen import LockScreenObject
from NVDAObjects.UIA import UIA
import NVDAState
from utils.security import getSafeScripts
from winAPI.sessionTracking import isLockScreenModeActive

"""App module for the Windows 10 and 11 lock screen.

The lock screen allows other windows to be opened, so security related functions
are done at a higher level than the lockapp app module.
Refer to usages of `winAPI.sessionTracking.isLockScreenModeActive`.
"""


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "LockAppObject" and NVDAState._allowDeprecatedAPI():
		log.warning(
			"lockapp.LockAppObject is deprecated, use NVDAObjects.lockscreen.LockScreenObject instead.",
		)
		return LockScreenObject
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


# Windows 10 and 11 lock screen container
class LockAppContainer(UIA):
	# Make sure the user can get to this so they can dismiss the lock screen from a touch screen.
	presentationType = UIA.presType_content


class AppModule(appModuleHandler.AppModule):
	SAFE_SCRIPTS = getSafeScripts()
	"""
	Deprecated, use utils.security.getSafeScripts() instead.
	"""

	def chooseNVDAObjectOverlayClasses(
		self,
		obj: NVDAObject,
		clsList: List[NVDAObject],
	) -> None:
		if (
			isinstance(obj, UIA)
			and obj.role == controlTypes.Role.PANE
			and obj.UIAElement.cachedClassName == "LockAppContainer"
		):
			clsList.insert(0, LockAppContainer)

		if not isLockScreenModeActive():
			log.debugWarning(
				"LockApp is being initialized but NVDA does not expect Windows to be locked. "
				"DynamicNVDAObjectType may have failed to apply LockScreenObject. "
				"This means session lock state tracking has failed. ",
			)
			clsList.insert(0, LockScreenObject)

	def event_foreground(self, obj: NVDAObject, nextHandler: Callable[[], None]):
		"""Set mouse object explicitly before continuing to the next handler.
		This is to prevent the mouse focus remaining on the desktop when locking the screen.
		"""
		api.setMouseObject(obj)
		nextHandler()

	def _inputCaptor(self, gesture: inputCore.InputGesture) -> bool:
		script = gesture.script
		if not script:
			return True
		scriptShouldRun = script in getSafeScripts()
		if not scriptShouldRun:
			log.error(
				"scriptHandler failed to block script when Windows is locked. "
				"This means session lock state tracking has failed. ",
			)
		return scriptShouldRun

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
