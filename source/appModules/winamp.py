#appModules/winamp.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.IAccessible import IAccessible 
import appModuleHandler

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="Winamp v1.x":
			obj.__class__=winampMainWindow

class winampMainWindow(IAccessible):

	def event_nameChange(self):
		pass

	def event_gainFocus(self):
		pass
