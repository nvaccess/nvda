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
		if controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ("TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl") and not obj.role in (controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU):
			obj.value=None
