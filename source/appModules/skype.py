# -*- coding: UTF-8 -*-
#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2013 Peter Vágner, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import winUser

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_MENUBAR):
			# The window handle reported by Skype accessibles is sometimes incorrect.
			# This object is focused, so we can override with the focus window.
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ("TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl"):
			# The name and value both include the user's name, so kill the value to avoid doubling up.
			# The value includes the Skype name,
			# but we care more about the additional info (e.g. new event count) included in the name.
			obj.value=None
