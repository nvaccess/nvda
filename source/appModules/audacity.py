#appModules/audacity.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import winUser

class appModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="Button":
			obj.name=winUser.getWindowText(obj.windowHandle).replace('&','')
