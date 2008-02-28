#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if (obj.windowClassName=="TMainUserList") or (obj.windowClassName=="TPanel" and obj.windowControlID==13698186):
			obj.name=obj.value
			obj.value=None
