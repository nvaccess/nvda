#appModules/audacity.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import winUser
import controlTypes
from NVDAObjects.IAccessible import edit

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		if controlTypes.STATE_FOCUSED in obj.states:
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.windowClassName=="Button" and not obj.role in [controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU]:
			obj.name=winUser.getWindowText(obj.windowHandle).replace('&','')
		elif obj.windowClassName=="Edit" and obj.role==controlTypes.ROLE_EDITABLETEXT:
			obj.__class__=edit.Edit
