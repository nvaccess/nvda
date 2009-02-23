#appModules/audacity.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import winUser
import controlTypes
from NVDAObjects.window import edit

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="Button" and not obj.role in [controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU]:
			obj.name=winUser.getWindowText(obj.windowHandle).replace('&','')
