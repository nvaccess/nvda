#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import winUser

class appModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if controlTypes.STATE_FOCUSED in obj.states:
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ["TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList"] and not obj.role in [controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU]:
			obj.name=obj.value
			obj.value=None
