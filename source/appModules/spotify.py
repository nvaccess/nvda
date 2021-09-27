#appModules/spotify.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013-2017 NV Access Limited, James Teh

"""App module for Spotify
"""

import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible import IAccessible
import eventHandler

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "Chrome_RenderWidgetHostHWND" and isinstance(obj, IAccessible) and obj.IAccessibleChildID < 0 and obj.role == controlTypes.Role.UNKNOWN:
			# #5439: Focus seems to hit Chromium objects that die before we can fetch them.
			obj.shouldAllowIAccessibleFocusEvent = False

	def event_gainFocus(self, obj, nextHandler):
		if not eventHandler.isPendingEvents("gainFocus") and obj.windowClassName == "Chrome_WidgetWin_0" and obj.role == controlTypes.Role.WINDOW:
			# Spotify doesn't fire focus on the correct object when it gets the foreground.
			# Instead, it fires focus on a window ancestor.
			# Try to get the correct focus.
			try:
				focus = obj.firstChild.firstChild.activeChild
			except AttributeError:
				focus = None
			if focus:
				# Bounce focus to the correct object.
				return eventHandler.executeEvent("gainFocus", focus)
		return nextHandler()
